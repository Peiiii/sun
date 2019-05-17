import piudb,uuid,time,config
from piudb import Model,StringField,TableManager,TextField,ObjectField,BooleanField,IntegerField,Field,FloatField,Piu
def next_id():
    t=time.gmtime()
    id=str(t.tm_year)+str(t.tm_mon)+str(t.tm_mday)+(uuid.uuid4().hex)
    return id

class Blog(Model):

    id=StringField(primary_key=True,default=next_id)
    title=StringField()
    text=TextField(searchable=False)
    html=TextField(searchable=False)
    content=TextField(searchable=False)
    digest=TextField()
    category=StringField()
    tags=ObjectField()
    archieve=StringField()
    author=StringField(default='WP')
    created_at=FloatField(default=time.time)

    mood=StringField()
    status=StringField()
    visible=BooleanField()
    description=StringField()
    length=IntegerField()
    num_words=IntegerField()
    views=IntegerField(default=0)
    stars=IntegerField(default=0)
    year=StringField()
    month=StringField()
    day=StringField()
    fields=ObjectField()
    info=ObjectField()
    default_template=StringField(config.page_templates.article)

    def addDefault(self):
        self.addID()
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
