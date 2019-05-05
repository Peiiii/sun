import asyncio, config, pickle, os, time, uuid
from tools import loadText, writeFile, getLine,log
from config import dirs
from orm import Table
'''
config here
'''
blogs_dir=config.other_config.blogs_dir
mapfile_name=config.other_config.mapfile_name
defalut_blog_template=config.other_config.defalut_blog_template
users_dir=config.other_config.users_dir
tableUser=Table(path=users_dir,primary_key='id',searchable_keys=['email','nick_name','id','password','image','admin','info','description'])
class MyDict(dict):
    def __getattr__(self, item):
        return self[item]

class User:
    __table__=tableUser
    def __init__(self,id,email,password,nick_name,image='ablout:blank',
                 description='',signature='',admin=False,info='',fields=[]):
        self.id=id
        self.email=email
        self.password=password,
        self.nick_name=nick_name,
        self.image=image,
        self.description=description
        self.signature=signature
        self.admin=admin
        self.info=info
        self.fields=fields
    def toJson(self):
        dic=self.__dict__
        json={}
        for k in dic:
            json[k]=self.__getattribute__(k)
        return json

class Blog:
    def __init__(self,
                 title, text , html, created_at, category, tags=[],id=None,author='',visible=True,
                 description='',length=None,views=None,stars=None, info='',fields={},display_template=defalut_blog_template
                 ):
        self.title = title
        self.text=text
        self.html=html
        self.created_at = created_at
        t = time.localtime(created_at)
        self.archieve = str(t.tm_year) + '年' + str(t.tm_mon) + '月'
        self.category = category
        self.tags = tags
        self.author=author
        self.visible=visible
        self.description=description
        self.length=length
        self.views=views
        self.stars=stars
        self.info=info
        self.fields=fields
        self.display_template=display_template
        if not id:
            self.id = uuid.uuid4().hex
        else:
            self.id = id
    def toJson(self):
        dic=self.__dict__
        json={}
        for k in dic:
            json[k]=self.__getattribute__(k)
        return json
    def shortCut(self):
        return MyDict(
            title=self.title,id=self.id,archieve=self.archieve,author=self.author,description=self.description
        )

class BlogManager2(Table):
    def __init__(self,path,primary_key=None,searchable_keys=None):
        if not primary_key:
            primary_key='id'
        if not searchable_keys:
            searchable_keys=['id','title','author','created_at','archieve','category','description',
                                           'tags','info','visible','views','stars']
        super().__init__(path,primary_key,searchable_keys)
    async def loadBlogs(self):
        blogs=await self.findAll()
        return blogs
    async def saveBlog(self,blog):
        if not await self.exsist(blog.id):
            return await self.insert(blog)
        return self.replace(blog.id,blog)
    async def deleteBlog(self,id):
        return await self.delete(id)
    async def getBlogByID(self,id):
        return await self.find(id)
    async def rebuild(self):
        pass


class BlogManger:
    def __init__(self,path=None):
        if not path:
            self.workpath=blogs_dir
        else:
            self.workpath=path
        if(not os.path.exists(self.workpath)):
            os.mkdir(self.workpath)
        self.mapfile=self.workpath+'/'+mapfile_name


    def _load(self, file):
        try:
            f = open(file, 'rb')
            blog = pickle.load(f)
            return blog
        except:
            return False
    async def exsist(self,id=None,title=None):
        map=self.getMap()
        if id:
            title= map.get(id,False)
            if title:
                return title
            return False
        if title:
            if title in map.values():
                return True
            return False
    def _getBlogByTitle(self,title):
        return self._load(self.workpath+'/'+title+'.blog')
    async def getBlogByTitle(self,title):
        if not await self.exsist(title=title):
            return False
        return self._getBlogByTitle(title)
    def _getBlogByID(self,id):
        map=self.getMap()
        title=map[id]
        return self._getBlogByTitle(title)
    async def getBlogByID(self,id):
       if not await self.exsist(id=id):
           return False
       return self._getBlogByID(id)
    def _saveBlog(self,blog):
        fname = self.workpath + '/' + blog.title + '.blog'
        f = open(fname, 'wb')
        pickle.dump(blog, f)
        map = self.getMap()
        map[blog.id] = blog.title
        self.saveMap(map)
        return True
    async def saveBlog(self, blog):
        log('saving blog:',blog.shortCut())
        return self._saveBlog(blog)


    async def loadBlogs(self):
        map=self.getMap()
        bug=False
        blogs = []
        for f in map.values():
            fpath = self.workpath+'/'+f+'.blog'
            blog = self._load(fpath)
            if blog:
                blogs.append(blog)
            else:
                bug=True
        if bug:
            log('There is a Bug . from load blogs')
            # await self.rebuild()
        return blogs
    def getMap(self):
        try:
            f=open(self.mapfile,'rb')
            map = pickle.load(f)
        except:
            f=open(self.mapfile,'wb')
            map={}
        f.close()
        return map
    def saveMap(self,map):
        f=open(self.mapfile,'wb+')
        pickle.dump(map,f)
        f.close()
    async def deleteBlog(self,id):
        map=self.getMap()
        fname=map.get(id,'notfound')
        if fname=='notfound':
            return False
        map.pop(id)
        fname=self.workpath+'/'+fname+'.blog'
        os.remove(fname)
        self.saveMap(map)
        log('delete blog: id= %s ,fname=%s'%(id,fname))
        return True
    async def rebuild(self):
        blogs= await loadBlogs()
        map={}
        for b in blogs:
            map[b.id]=b.title
        self.saveMap(map)
        log('rebuild success. map:',map)
    async def update(self,id,**kws):
        pass




async def loadBlog(file):
    f = open(file, 'rb')
    blog = pickle.load(f)
    checkID(blog)
    return blog


async def saveBlog(blog):
    fname = config.dirs.blogs + '/' + blog.title + '.blog'
    f = open(fname, 'wb')
    return pickle.dump(blog, f)


async def loadBlogs():
    blog_dir = config.dirs.blogs
    children = os.listdir(blog_dir)
    blogs = []
    for f in children:
        fpath = blog_dir + '/' + f
        if (not os.path.isfile(fpath)):
            continue
        if (len(f) < 5 or f[-5:].lower() != '.blog'):
            continue
        blog = await loadBlog(fpath)
        if blog:
            blogs.append(blog)
    return blogs


########--------------------temprory tools---------------------
def getAttr(obj, attr):
    try:
        v = obj.__getattribute__(attr)
        return v
    except:
        return None


def hasAttr(obj, attr):
    try:
        obj.__getattribute__(attr)
        return True
    except:
        return False


def checkID(blog):
    if not hasAttr(blog, 'id'):
        blog.id = uuid.uuid4().hex
