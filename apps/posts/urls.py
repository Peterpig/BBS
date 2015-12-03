# -*- coding: utf-8 -*-
from django.conf.urls.defaults  import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.posts.posts',
    (r'^t/(?P<id>\d+)/$', 'index'),    # 文章单页
    (r'new/$', 'new'),   # 发表新文章
    (r'upload_img/$', 'upload_img'),   # 发表新文章
    (r'post_vote/$', 'post_vote'),      # 投票按钮
    (r'add_option/$', 'add_option'),      # 添加选项
    )
