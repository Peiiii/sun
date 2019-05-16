import config,tools,time,os
from  jinja2 import  Template,Environment, PackageLoader
from models import TableOpener,Blog


templates_dir=config.other_config.templates_dir
env = Environment(loader=PackageLoader(templates_dir,''))
opener=TableOpener()
tb=opener.open(config.db_dir_blogs,'a',Blog)

pre_make_dirs=config.pre_make_dirs


def rebuild():
    tools.allBlogsToHTML(tb=tb,env=env,path=config.articles_dir,template=config.page_templates.article,force=True)
    tools.saveBlogsToJsonFiles(tb=tb,dpath=config.json_articles_dir)
def getBlogsFromJsonFiles():
    blogs=tools.loadBlogsFromJsonFiles(config.json_articles_dir)
    [print(b['title']) for b in blogs.values()]
    return blogs
def rebuidFromTextFiles():
    # os.remove(config.db_dir_blogs)
    tools.loadBlogsFromTextFiles()
def make_dirs():
    for d in pre_make_dirs:
        if not os.path.exists(d):
            os.makedirs(d)

if __name__=="__main__":
    # rebuild()
    # getBlogsFromJsonFiles()
    rebuidFromTextFiles()
    pass