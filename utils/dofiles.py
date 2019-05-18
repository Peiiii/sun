import json,pickle,time,os

def writeJsonFile(obj,fpath):
    with open(fpath,'w') as f:
        json.dump(obj,f)
def loadJsonFile(fpath):
    with open(fpath,'r') as f:
        obj=json.load(f)
    return obj
def writeTextFile(fn, s, encoding='utf-8'):
    f = open(fn, 'wb')
    a = f.write(bytes(s, encoding=encoding))
    f.close()
    return a


def loadTextFile(file):
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