# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.index.index',
    (r'^index/$', 'index'),        # 首页
    (r'^$', 'wai_index'),        # 外首页
    (r'^download_file/$', 'download_file')
)
