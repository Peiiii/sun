import logging;logging.basicConfig(level=logging.INFO)
import asyncio,uuid,tools
from framework import Application,jsonResponse,apiError,pageResponse
from config import net,paths,dirs,pages
from models import Blog,loadBlog,saveBlog,loadBlogs,BlogManger
from tools import log

loop=asyncio.get_event_loop()
app=Application(loop=loop)
blman=BlogManger()

base_link='http://127.0.0.1:'+str(net.port)
quik_links=['/','/manage']
##---------------------Make handlers------------------
@app.get2(paths.root)
async def do_root():
    await blman.rebuild()
    blogs=await blman.loadBlogs()
    print(blogs)
    return pageResponse(template=pages.root,blogs=blogs)
@app.get2(paths.about)
async def do_about():
    ''' '''
    pass
@app.get2(paths.tags)
async def do_tags():
    ''' '''
    pass
@app.get2(paths.categories)
async def do_categories():
    ''' '''
    pass
@app.get2(paths.archieves)
async def do_archieves():
    ''' '''
    pass
@app.get2(paths.search)
async def do_search():
    ''' '''
    pass
@app.get2(paths.manage)
async def do_manage_get():
    blogs=await blman.loadBlogs()
    return pageResponse(template=pages.manage,blogs=blogs)
##----------------------Manage Pages---------------------##
## editor
import  time
@app.get2(paths.editor)
async def do_editor_get():
    return pageResponse(template=pages.editor)
@app.post4(paths.editor,json=True)
async def do_editor_get(title,md,category,tags):

    created_at=time.time()
    md=tools.textToHTML(md)
    b=Blog(
        title=title,md=md,created_at=created_at,category=category,tags=tags
    )
    # log(md)
    status=await blman.saveBlog(b)
    return jsonResponse(success=status,message='上传成功！')

## alter
@app.post5('/manage/alter')
async def do_manage_alter(json,opr_type):
    id=json['id']
    if opr_type=='delete':
        s=await blman.deleteBlog(id)
        print(s,id)
        if s:
            return jsonResponse(message='删除成功')
        return apiError(message='删除失败')

##------------------Make Handlers Details----------------##
async def getMds():
    pass
##---------------------End Make Handlers---------------------------##
app.router.add_static('/', 'static', show_index=True)
async def init(loop):
    server = await loop.create_server(app.make_handler(), net.ip, net.port)
    return server
loop.run_until_complete(init(loop))
for i in quik_links:
    print(base_link+i)
loop.run_forever()