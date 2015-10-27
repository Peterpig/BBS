# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^BBS/', include('BBS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_SITE}),
    (r'^crossdomain.xml$', 'django.views.generic.simple.direct_to_template', {'template': 'crossdomain.xml'}), # flash跨域访问文件
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_SITE}),
    (r'^upload_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^theme_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.THEME_SITE}),
)


urlpatterns += patterns('', 
    (r'', include('apps.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    )