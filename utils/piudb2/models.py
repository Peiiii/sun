
from .supported_classes import InfoBody
from .classes import *
import uuid
def flag():
    print('*'*20,'FLAG HERE','*'*20)
class Collection(list):
    def sortBy(self,key,reverse=True):
        li=sorted(self,key=lambda x: x[key] ,reverse=reverse)
        return li
def openAll():
    pass

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

    format_used=StringField(default='plain-text')
    content=TextField(searchable=False)
    digest=TextField()
    category=StringField()
    tags=ObjectField(default=[])
    archieve=StringField()
    author=StringField(default='')
    created_at=FloatField(default=time.time)
    location=StringField(default='')


    date=StringField()
    keywords=StringField()
    url=StringField()
    mood=StringField()
    status=StringField()
    visible=StringField(default='true')
    description=StringField()
    length=IntegerField()
    num_words=IntegerField()
    public=BooleanField(default=True)

    rank=IntegerField(default=0)
    views=IntegerField(default=0)
    stars=IntegerField(default=0)
    year=IntegerField(default=get_year)
    month=IntegerField(default=get_month)
    day=IntegerField(default=get_mday)
    fields=ObjectField()
    info=ObjectField()
    template=StringField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def checkDefault(self):
        self.checkAllFieldsByDefault()
        self.addID()
        self.addArchieve()
        self.addDigest()
        self.addDate()
        self.addKeywords()
        self.addDescription()

    def addDate(self):
        if not self.date or self.date=='':
            t=self.created_at
            self.date=self.convertDate(t)
    def addArchieve(self):
        if self.archieve=='':
            t=time.localtime(self.created_at)
            self.archieve=str(self.year)+'年'+str(self.month)+'月'
    def addID(self):
        t = time.gmtime()
        id = str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday)+self.title
        self['id'] =id
    def addDigest(self):
        if not self.digest or self.digest == '':
            text=self.text
            digest=text[:500] if len(text)>=500 else text
            self.digest=digest
    def addKeywords(self):
        if self.isEmpty(self.keywords):
            keywords=self.digest.split()
            if len(keywords)>=5:
                self.keywords=';'.join(keywords[:5])
            self.keywords=';'.join(keywords)
    def addDescription(self):
        if self.isEmpty(self.description):
            self.description=self.digest[:200] if len(self.digest)>=200 else self.digest
    def isEmpty(self,s):
        if not s or s.strip()=='':
                return True
        return False
    def convertDate(self,t):
        t=time.strftime('%Y-%m-%d',time.localtime(t))
        return t
    def toJson(self):
        dic=self.__fields__
        json={}
        for k in dic:
            json[k]=self.__getattr__(k)
        return json
    def shortCut(self):
        return InfoBody(
            title=self.title,id=self.id,archieve=self.archieve,author=self.author,description=self.description
        )
