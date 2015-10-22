# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.account.views',
     (r'^register/$', 'register'),       # 注册
     (r'^login/$', 'login_'),           # 登陆
     (r'^logout/$', 'logout_'),         # 登出
)