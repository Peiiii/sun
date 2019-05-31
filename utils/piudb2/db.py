from .classes import *
from .supported_classes import *

class DBOperator:
    pass
def createDB(path):
    mf=DB.mapfilename
    mpath=mf+'/'+mf
    if not os.path.exists(path):
        os.makedirs(path)
    mf=InfoBody(tables=[])
    writeObjectFile(mf,mpath)

class DB:
    mapfilename='mapfile.map'
    def __init__(self,dbpath):
        self.path=dbpath
        self.mpath=self._joinPath(DB.mapfilename)
        self.loadMapfile()
        self.loadTables()
    def _joinPath(self,childpath):
        return self.path+'/'+childpath
    def loadMapfile(self):
        self.map=readObjectFile(self.mpath)
    def loadTables(self):
        tables=[]
        for t in self.map:
            tb=Table(self._joinPath(t))
            tables.append(tb)
        self.tables=tables
