import piudb,uuid,time,config,asyncio
from piudb import (
    Model,StringField,TableManager,TextField,ObjectField,
    BooleanField,IntegerField,Field,FloatField,Piu,InfoBody,
    Piu
)

class Helper(InfoBody):
    def __init__(self,blog_tb,**kwargs):
        self.blog_tb=blog_tb
        self.tb=blog_tb
        assert isinstance(blog_tb,Piu)
        super().__init__(**kwargs)
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
    def rectifyTags(self):
        tags_lists=self.getAllFieldValues('tags',list_item=True)
        tag_names=[]
        for tags in tags_lists:
            print('tags:',tags)
            tag_names.append(tags)
        tag_names=list(set(tag_names))
        for name in tag_names:
            self.tag_tb._upsert_(Cluster(name=name))
            # self.tb.raiseError()
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
    def rectifyCategories(self):
        cates=self.getCategoryNames()
        for name in cates:
            self.cate_tb._upsert_(Category(name=name))
            # self.tb.raiseError()



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
    content=TextField(searchable=False)
    digest=TextField()
    category=StringField()
    tags=ObjectField(default=[])
    archieve=StringField()
    author=StringField(default='WP')
    created_at=FloatField(default=time.time)

    keywords=StringField()
    url=StringField()
    mood=StringField()
    status=StringField()
    visible=BooleanField()
    description=StringField()
    length=IntegerField()
    num_words=IntegerField()
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
    def addArchieve(self):
        if not self.archieve=='':
            t=time.gmtime(self.created_at)
            self.archieve=str(self.year)+'年'+str(self.month)+'月'
    def addID(self):
        t = time.gmtime()
        id = str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday)+self.title
        self['id'] =id
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
