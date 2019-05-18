import piudb,uuid,time,config,asyncio,markdown,bs4
from piudb import (
    Model,StringField,TableManager,TextField,ObjectField,
    BooleanField,IntegerField,Field,FloatField,Piu,InfoBody,
    Piu
)
class Collection(list):
    def sortBy(self,key,reverse=True):
        li=sorted(self,key=lambda x: x[key] ,reverse=reverse)
        return li
def openAll():
    from config import db
    helper=Helper()
    helper.blog_tb=Piu(db.path.blogs, Blog, auto_update_fields=True, overwrite_fields=True)
    helper.cate_tb=Piu(db.path.categories, Category, auto_update_fields=True, overwrite_fields=True)
    helper.tag_tb=Piu(db.path.tags, Cluster, auto_update_fields=True, overwrite_fields=True)
    helper.archieve_tb=Piu(db.path.archieves, Cluster, auto_update_fields=True, overwrite_fields=True)
    return helper
class Helper(InfoBody):
    def __init__(self,blog_tb=None,**kwargs):
        if blog_tb:
            self.blog_tb=blog_tb
            self.tb=blog_tb
            assert isinstance(blog_tb,Piu)
        super().__init__(**kwargs)
    def open(self,name,**kws):
        self[name]=Piu(**kws)
    def reBuild(self):
        blogs=self.blog_tb._findAll_()
        num=self.blog_tb._deleteAll_()
        print('num: %s'%num)
        for b in blogs:
            print('Blog deleted: %s'%b.title)
            self.blog_tb._insert_(b)
    async def getArchieves(self):
        archs=self.archieve_tb._findAll_()
        archs2=[]
        for a in archs:
            archs2.append(self.getCluster(cluster_name=a.name,archieve=a.name))
        return archs2

    def getCategoryNames(self):
        return self.getAllFieldValues('category')
    def getAllFieldValues(self,key,list_item=False):
        tb = self.blog_tb
        ibs = tb._select_([key])
        values = [ib[key] for ib in ibs]
        if not list_item and  not isinstance(values[0],list):
            values=list(set(values))
            print(values)
            return values
        vs=[]
        for v in values:
            vs+=v
        return vs
    def quikInsert(self,blog):
        self.blog_tb._insert_(blog)
    def getCluster(self,cluster_name,checker=None,**kws):
        if checker and callable(checker):
            kws['__checker__']=checker
        blogs=self.blog_tb._findAll_(**kws)
        length=len(blogs)
        return Cluster(name=cluster_name,blogs=blogs,length=length)

    async def getTags(self):
        assert isinstance(self.tag_tb,Piu)
        tags=self.tag_tb._findAll_()
        new_tags=[]
        for t in tags:
            def checker(record):
                if t.name in record['tags']:
                    return True
                else:
                    return False
            tag=self.getCluster(cluster_name=t.name,checker=checker)
            if not tag.length:
                continue
            new_tags.append(tag)
        return new_tags

    async def getCategories(self):
        cs = self.cate_tb._findAll_()
        cates = []
        for c in cs:
            cate = self.getCluster(cluster_name=c.name, category=c.name)
            if not cate.length:
                continue
            cates.append(cate)
        return cates
    def fixAll(self):
        self.rectifyCategories()
        self.rectifyTags()
        self.rectifyArchieves()
    def rectifyCategories(self):
        cates=self.getCategoryNames()
        for name in cates:
            self.cate_tb._upsert_(Category(name=name))
            # self.tb.raiseError()

    def rectifyTags(self):
        tags_lists = self.getAllFieldValues('tags', list_item=True)
        tag_names = []
        for tags in tags_lists:
            print('tags:', tags)
            tag_names.append(tags)
        tag_names = list(set(tag_names))
        for name in tag_names:
            if not name or name=='':
                continue
            self.tag_tb._upsert_(Cluster(name=name))
            # self.tb.raiseError()
    def rectifyArchieves(self):
        archs = self.getAllFieldValues('archieve')
        print('rtf archieves:',archs)
        for a in archs:
            arch=Cluster(name=a)
            self.archieve_tb._insert_(arch)

class Category(Model):
    name=StringField(primary_key=True)
    length=IntegerField()
    blogs=ObjectField(default=[])

    def getLength(self):
        self.length=len(self.blogs)

class Cluster(Model):
    name=StringField(primary_key=True)
    length=IntegerField()
    blogs=ObjectField(default=[])

    def __init__(self,**kws):
        super().__init__(**kws)
    def getLength(self):
        self.length=len(self.blogs)




def next_id():
    t=time.gmtime()
    id=str(t.tm_year)+str(t.tm_mon)+str(t.tm_mday)+(uuid.uuid4().hex)
    return id
def get_year():
    return time.gmtime().tm_year
def get_month():
    return time.gmtime().tm_mon
def get_mday():
    return time.gmtime().tm_mday
class Blog(Model):

    id=StringField(primary_key=True,default=next_id)
    title=StringField()
    text=TextField(searchable=False)
    html=TextField(searchable=False)
    md=TextField(searchable=False)

    format_used=StringField(default='text/plain')
    content=TextField(searchable=False)
    digest=TextField()
    category=StringField()
    tags=ObjectField(default=[])
    archieve=StringField()
    author=StringField(default='WP')
    created_at=FloatField(default=time.time)


    date=StringField()
    keywords=StringField()
    url=StringField()
    mood=StringField()
    status=StringField()
    visible=BooleanField()
    description=StringField()
    length=IntegerField()
    num_words=IntegerField()


    rank=IntegerField(default=0)
    views=IntegerField(default=0)
    stars=IntegerField(default=0)
    year=IntegerField(default=get_year)
    month=IntegerField(default=get_month)
    day=IntegerField(default=get_mday)
    fields=ObjectField()
    info=ObjectField()
    default_template=StringField(config.page_templates.article)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def checkDefault(self):
        self.checkAllFieldsByDefault()
        self.addID()
        self.addArchieve()
        self.addDigest()
        self.addDate()
    def addDate(self):
        if not self.date or self.date=='':
            t=self.created_at
            self.date=self.convertDate(t)
    def addArchieve(self):
        if self.archieve=='':
            t=time.gmtime(self.created_at)
            self.archieve=str(self.year)+'年'+str(self.month)+'月'
    def addID(self):
        t = time.gmtime()
        id = str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday)+self.title
        self['id'] =id
    def addDigest(self):
        if not self.digest or self.digest == '':
            text=bs4.BeautifulSoup(self.html).text
            digest=text[:500] if len(text)>=500 else text
            self.digest=digest
    def convertDate(self,t):
        t=time.strftime('%Y-%m-%d',time.gmtime(t))
        return t
    def toJson(self):
        dic=self.__fields__
        json={}
        for k in dic:
            json[k]=self.__getattr__(k)
        return json
    def shortCut(self):
        return piudb.InfoBody(
            title=self.title,id=self.id,archieve=self.archieve,author=self.author,description=self.description
        )
