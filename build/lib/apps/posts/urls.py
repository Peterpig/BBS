# -*- coding: utf-8 -*-
from django.conf.urls.defaults  import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.posts.posts',
    (r'^t/(?P<id>\d)', 'index'),    # 文章单页
    (r'new/$', 'new'),   # 发表新文章
    )