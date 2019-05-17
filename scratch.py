from models import Blog
import piudb
from piudb import Piu
# from utils.mydb import TableManager

test_dir='data/db/test_table'
tb2=piudb.Piu(test_dir,Blog)



def test1():
    blogs = tb1._findAll_()
    [print(i.title) for i in blogs]
    for b in blogs:
        dic={}
        for k in b.__fields__:
            dic[k]=b.get(k)
        b2=Blog2(**dic)
        tb2._insert_(b2)
def test2():
    global tb2
    a=tb2._insert_(Blog(title='hu'))
    print(a)
    blogs=tb2._findAll_()
    [print(i.title) for i in blogs]
    print(tb2.tb.map.dic)
    tb2=Piu(test_dir,Blog)
    print(tb2.tb.map.dic)




if __name__ == "__main__":
    # test1()
    test2()
    pass