# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('apps.index.urls')),
    (r'^t/(?P<id>\d)', include('apps.posts.urls')),
)


urlpatterns += patterns('',
     (r'^signup/$', 'apps.account.views.signup'),       # 注册
     (r'^login/$', 'apps.account.views.login'),         # 登陆
)