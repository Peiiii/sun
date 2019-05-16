import piudb
from models import Blog
opener=piudb.TableOpener()
tb=opener.open('data/db/blogs','l',Blog)
a=tb._findAll_()
[print(i.title) for i in a]
