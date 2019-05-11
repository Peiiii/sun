
class Config(dict):
    def __getattr__(self, item):
        try:
            r=self.__getitem__(item)
            return r
        except:
            raise AttributeError('No attribute %s'%item)

admin=Config(
    name='top',
    password='password',
    id='00000000001',
    email='1535376447@qq.com'
)
net=Config(
    ip='0.0.0.0',
    port=80,
    domain='localhost'
)

dirs=Config(
    blogs='../blogs'
)
other_config=Config(
    blogs_dir='../blogs',
    templates_dir='templates',
    mapfile_name='mapfile.map',
    show_index=True,
    defalut_blog_template='lib/html/blog.html',
    users_dir='../users'
)

paths=Config(
    root='/',
    about='/about',
    tags='/tags',
    categories='/categories',
    archieves='/archieves',
    search='/search',
    manage='/manage',
    editor='/manage/editor',
)

pages=Config(
    root='pages/home/home.html',
    about='pages/about/about.html',
    tags='pages/tags/tags.html',
    categories='pages/categories/categories.html',
    archieves='pages/archieves/archieves.html',
    search='pages/search/search.html',
    manage='pages/manage/manage.html',
    error='pages/error/error.html'
)

