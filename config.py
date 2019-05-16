
class Config(dict):
    def __getattr__(self, item):
        try:
            r=self.__getitem__(item)
            return r
        except:
            raise AttributeError('No attribute %s'%item)


articles_dir='static/p'
static_path=['static']
default_article_template='pages/article/article.html'
db_dir_blogs='../db/blogs'
json_articles_dir='data/json/articles'
text_articles_dir='data/text/articles'

pre_make_dirs=[json_articles_dir,articles_dir]

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
    article='/p'
)

pages=Config(
    root='pages/home/home.html',
    article='pages/article/article.html',
    about='pages/about/about.html',
    tags='pages/tags/tags.html',
    categories='pages/categories/categories.html',
    archieves='pages/archieves/archieves.html',
    search='pages/search/search.html',
    manage='pages/manage/manage.html',
    error='pages/error/error.html'
)

page_templates=Config(
    root='pages/home/home.html',
    article='pages/article/article.html',
    about='pages/about/about.html',
    tags='pages/tags/tags.html',
    categories='pages/categories/categories.html',
    archieves='pages/archieves/archieves.html',
    search='pages/search/search.html',
    manage='pages/manage/manage.html',
    error='pages/error/error.html'
)

