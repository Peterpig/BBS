# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('apps.index.urls')),
    (r'', include('apps.posts.urls')),
)


urlpatterns += patterns('',
     (r'', include('apps.account.urls')),         # 注册登陆
)

urlpatterns += patterns('',
     (r'^member/', include('apps.account.urls')),         # 注册登陆
)
