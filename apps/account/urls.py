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

urlpatterns += patterns('apps.account.account',
     (r'^(?P<name>\w+)/$', 'user_index'),       # 个人中心
     (r'^profile/change_header_img/$', 'change_header_img'),       # 个人中心
)
