from django.conf.urls.defaults import *

from blog import views, models


urlpatterns = patterns('',
    # blog post
    url(r'^article/(?P<username>[-\w]+)/(?P<slug>[-\w]+)/$', 'blog.views.article', name='article'),

    # all blog posts
    url(r'^$', 'blog.views.blogs'),

    # your articles
    url(r'^yourarticles/$', 'blog.views.yourarticles', name="your_articles"),
    
    # new blog post
    url(r'^new/$', 'blog.views.new'),
    
    # edit blog post
    url(r'^edit/(\d+)/$', 'blog.views.edit', name="edit_post"),
)
