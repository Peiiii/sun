import os, time,hashlib,markdown,re
import asyncio
import  utils.spider as spider
from orm import InfoBody
from models import  Blog,BlogManager2
blman=BlogManager2(path='../db/Myblogs')
articles_dir='data/articles'
def initTools():
    pass


##----------------End Specific Tools----------##
def log(*args, num=20, str='*'):
    print(str * num, end='')
    print(*args, end='')
    print(str * num)
def getLineNum(text):
    return text.find('\n')
def getLine(text,n):
    num=getLineNum(text)
    if n>=num:
        return False
    else:
        return text.split('\n')[n]
def writeFile(fn, s, encoding='utf-8'):
    f = open(fn, 'wb')
    a = f.write(bytes(s, encoding=encoding))
    f.close()
    return a


def loadText(file):
    import chardet
    f = open(file, 'rb')
    text = f.read()
    f.close()
    encoding = chardet.detect(text)['encoding']
    if text:
        text = text.decode(encoding=encoding)
    else:
        text = ''
    return text


def formatTime( t):
    t = time.localtime(t)
    return time.strftime('%Y/%m/%d  %H:%M:%S', t)

def encrypt(*args):
    text=':'.join(args)
    encrypted=hashlib.sha1(text.encode('utf-8')).hexdigest()
    return encrypted
def textToHTML(text):
    text,dic=renderDocument(text)
    format=dic.get('format',None)
    format=format or 'text/plain'

    if format=='text/plain' :
        text=text.split('\n')
        new_text = []
        for i in text:
            new_text.append('<p>' + i + '</p>')
        return '\n'.join(new_text)
    elif format=='md' or format=='markdown':
        return mdToHTML(text)
def textToDic(text,divider=';',equal_char='='):
    text=text.strip().strip(divider)
    fields=text.split(divider)
    dic={}
    for f in fields:
        [name,value]=f.strip().split(equal_char)
        name=name.strip()
        value=value.strip()
        dic[name]=value
    return dic
def getHeadAndBody(text):
    text=text.strip()
    pat=re.compile('^/\*.*\*/',re.DOTALL)
    m=re.match(pat,text)
    if not m:
        return None,text
    body=re.sub(pat,'',text,count=1).strip()
    head=m.group(0).strip('/*').strip('*/')
    return head,body

from markdown import markdown
def mdToHTML(md):
    md=markdown(md)
    return md
def renderDocument(text):
    head,body=getHeadAndBody(text)
    if not head:
        return body,{}
    dic=textToDic(head)
    return body,dic

class PathType:
    def __init__(self):
        self.F = 'FILE'
        self.D = 'DIR'
        self.L = 'LINK'
        self.M = 'MOUNT'


T = PathType()


class Path:
    def __init__(self, path):
        self.path = path
        self.epath = self.encodePath()
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)
        self.atime = formatTime(os.path.getatime(path))
        self.ctime = formatTime(os.path.getctime(path))
        self.mtime = formatTime(os.path.getmtime(path))
        self.type = self.getType()

    def getType(self):
        if os.path.isdir(self.path):
            return T.D
        if os.path.isfile(self.path):
            return T.F
        if os.path.islink(self.path):
            return T.L
        if os.path.ismount(self.path):
            return T.M

    def encodePath(self):
        return self.path.replace('/', '%2F')

    def children(self):
        if self.type == T.D:
            list = self.listdir()
            return [Path(i) for i in list]

    def getContent(self):
        if self.type == T.F:
            return loadText(self.path)

    def listdir(self):
        if self.type == T.D:
            l = os.listdir(self.path)
            return [self.path + '/' + i for i in l]

    def fileChildren(self):
        list = self.children()
        return [i for i in list if i.type == T.F]

    def dirChildren(self):
        list = self.children()
        return [i for i in list if i.type == T.D]

    def linkChildren(self):
        list = self.children()
        return [i for i in list if i.type == T.L]

    def mountChildren(self):
        list = self.children()
        return [i for i in list if i.type == T.M]
    def toJson(self):
        return self.__dict__
    def addContent(self):
        self.content=self.getContent()


# p=Path('e:/webapp/www/templates')
# print(p.__dict__)
##---------------------------------------##

##-------------------Specific Tools------------##
def loadTestBlogs():
    files=os.listdir(articles_dir)
    articles=[]
    for f in files:
        art=loadBlogFromTextFile(articles_dir+os.sep+f)
        articles.append(art)
    return articles
def loadBlogFromTextFile(f):
    with open(f,'r',encoding='utf-8') as f:
        content=f.read()
        f.close()
    items=content.split('<$$$$$>')
    [title,intro,info,content]=items
    blog=InfoBody(title=title,intro=intro,info=info,content=content)
    # print(blog)
    return blog
async def addTestBlogs():
    articles=loadTestBlogs()
    for a in articles:
        blog=Blog(title=a.title,description=a.intro,info=a.info,text=a.content,category='Demo',html=textToHTML(a.content),created_at=time.time())
        await blman.saveBlog(blog,identified_by_title=True)
def initTest():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(addTestBlogs())
    loop.close()
if __name__=="__main__":
    # spider.makeArticles()
    initTest()


##----------------------------------------------------------------------------##
##----------------------------------------------------------------------------##

#####专用小工具
def parsePapers(text):
    lines=text.split('\n')
    lines=[l.strip() for l in lines]
    new_lines=[]
    for i in lines:
        if i == '' or i == '\n' or i[0]=='#':
            continue
        else:
            new_lines.append(i)
    lines=new_lines
    lines=[l.title() for l in lines]
    lines.sort()
    print('records: %s'%len(lines))
    return lines
def getPaperList(pfile):
    text=loadText(pfile)
    lines=parsePapers(text)
    return lines


