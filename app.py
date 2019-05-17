import logging;logging.basicConfig(level=logging.INFO)
import asyncio,uuid,tools,config
from framework import Application,jsonResponse,apiError,pageResponse
from config import net,paths,dirs,pages,other_config
from models import Blog,Piu
from tools import log
from aiohttp import web
from  jinja2 import  Template,Environment, PackageLoader


templates_dir=config.other_config.templates_dir
env = Environment(loader=PackageLoader(templates_dir,''))

loop=asyncio.get_event_loop()
app=Application(loop=loop)
blman=Piu('../db/blogs',Blog)


base_link='http://127.0.0.1:'+str(net.port)
quik_links=['/','/manage','/wp']


##---------------------Make handlers------------------
@app.get2(paths.root)
async def do_root():
    # await blman.rebuild()
    blogs=await blman.findAll()
    return pageResponse(template=pages.root,blogs=blogs)
@app.get2('/wp')
async def do_wp():
    headers={'location':'http://oneday.red:8000'}
    return web.Response(status=308,headers=headers)
# @app.get2(paths.article)
# async def do_article():
#     return pageResponse(template=pages.article)
@app.get2(paths.about)
async def do_about():
    return pageResponse(template=pages.about)
@app.get2(paths.tags)
async def do_tags():
    return pageResponse(template=pages.tags)
@app.get2(paths.categories)
async def do_categories():
    cates=await blman.getCategories()
    return pageResponse(template=pages.categories,categories=cates)
@app.get2(paths.archieves)
async def do_archieves():
   return pageResponse(template=pages.archieves)
@app.get2(paths.search)
async def do_search():
    return pageResponse(template=pages.search)
@app.get2(paths.manage)
async def do_manage_get():
    blogs=await blman.findAll()
    return pageResponse(template=pages.manage,blogs=blogs)
##----------------------Manage Pages---------------------##
## editor
import  time
@app.get2(paths.editor)
async def do_editor_get():
    return pageResponse(template=pages.editor)
@app.post5(paths.editor)
async def do_editor_post(title,md,html,description,author,info,category,tags,opr_type,id):
    created_at=time.time()
    text=md
    html=tools.textToHTML(text)
    b=Blog(
        title=title,text=text,html=html,created_at=created_at,category=category,tags=tags,id=id,author=author
    )
    await blman.insert(b)
    return jsonResponse(success=True,message='上传成功！')

## alter
@app.post5('/manage/alter')
async def do_manage_alter(json,opr_type):
    id=json['id']
    if opr_type=='delete':
        s=await blman.delete(id)
        if s:
            return jsonResponse(message='删除成功')
        return apiError(message='删除失败')
@app.post5('/manage/get_blog')
async def do_get_blog(blog_id):
    blog=await blman.findByPK(blog_id)
    if blog:
        return jsonResponse(data=blog.toJson())
    return apiError(message='blog not found.')
##------------------Make Handlers Details----------------##

##---------------------End Make Handlers---------------------------##
app.router.add_static('/', 'static', show_index=other_config.show_index)
async def init(loop):
    server = await loop.create_server(app.make_handler(), net.ip, net.port)
    return server
loop.run_until_complete(init(loop))
for i in quik_links:
    print(base_link+i)
loop.run_forever()