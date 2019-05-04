import os,pickle

class DBDirectory:
    def __init__(self,path,initial=False):
        self.path=os.path.abspath(path)
        self.mapfile=self.path+os.sep+os.path.basename(self.path)+'.map'
        if initial==True:
            self.makeSelf()
    def makeSelf(self):
        os.mkdir(self.path)
        map=[]
        self._writePickleFile(map,self.mapfile)
    def addFile(self,content,fname):
        self._writePickleFile(content,self._abspath(fname))
        map=self._getMap()
        map.append(fname)
        self._saveMap(map)
    def removeFile(self,fname):
        os.remove(self._abspath(fname))
        map=self._getMap()
        map.remove(fname)
        self._saveMap(map)
    def _rebuild(self):
        files=os.listdir(self.path)
        files.remove(os.path.basename(self.mapfile))
        self._saveMap(files)
    def _getMap(self):
        map=self._loadPickleFile(self.mapfile)
        return map
    def _saveMap(self,map):
        self._writePickleFile(map,self.mapfile)
    def _abspath(self,fname):
        return self.path+os.sep+os.path.basename(fname)

    def _loadPickleFile(self,fpath):
        f=open(fpath,'rb')
        obj=pickle.load(f)
        f.close()
        return obj
    def _writePickleFile(self,obj,fpath):
        f=open(fpath,'wb')
        ret=pickle.dump(obj,f)
        f.close()
        return ret


class Database:
    def __init__(self,path):
        self.path=path
    def initialize(self):
        pass

