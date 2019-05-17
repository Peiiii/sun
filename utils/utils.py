
import pickle,os,asyncio,json,time,uuid
TEST_MODE=True

def tlog(*args,**kwargs):
    try:
        if TEST_MODE:
            return log(*args,**kwargs)
    except:
        print('********warning , "TEST_MODE" is not setted in the module, which is needed to run "tlog()" ')
def log(*args, num=20, str='*'):
    print(str * num, end='')
    print(*args, end='')
    print(str * num)
def writeObjectFile(obj,fpath):
    f=open(fpath,'wb')
    pickle.dump(obj,f)
    f.close()
def readObjectFile(fpath):
    f=open(fpath,'rb')
    try:
        obj=pickle.load(f)
    except:
        print(fpath)
        raise
    return obj