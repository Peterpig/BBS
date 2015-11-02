#!/usr/bin/env python
#coding=utf-8
import logging, traceback, os

from django.http import HttpResponseRedirect
from django.conf import settings as _settings

log = logging.getLogger(__name__)

anonymous_urls = ['/site_media/', '/media/', '/theme_media/', '/upload_media/']

login_urls = ['/account/improve_user/', '/account/improve_user_submit',
              '/book/', '/post/error_feedback/', 
              ]

class AuthenticationMiddleware(object):
    def process_request(self, request):
        path = str(request.path)
        
        if path == '/':
            return
        
        for obj in anonymous_urls:
            if path.startswith(obj):
                return
        
        user = request.user
        
        #需要登录访问
        if user.is_anonymous(): #未登陆跳转首页
            # if path == "/summer/math/" or path == "/summer/english/":
            #     return
            if path in login_urls:
                return HttpResponseRedirect('/login/?url=%s' % path)   #   ('%s/' % _settings.URLROOT)

    def process_exception(self, request, exception):
        """
        功能说明:view函数抛出异常处理
        -------------------------------
        修改人     修改时间
        --------------------------------
        徐威      2013-07-17
        """
        path = str(request.path)

        if isinstance(exception, Http404):
            return
        if isinstance(exception, AssertionError):
            message = exception.message
            if not message:
                return
            if isinstance(message, Redirect):
                return HttpResponseRedirect(message.url)
            if isinstance(message, Http404):
                raise message
            raise Http404('AssertionError: %s' % exception.message)
        if isinstance(exception, Redirect):
            return HttpResponseRedirect(exception.url)
        
        # 如果请求的路径为 js css 文件 不处理
        if path.startswith('/site_media/'):
            return None
        if path.startswith('/media/'):
            return None
        # 如果请求的路径为 js css 文件 不处理
        if path.startswith('/theme_media/'):
            return None
        # 如果请求的路径为 js css 文件 不处理
        if path.startswith('/upload_media/'):
            return None

        exc = traceback.format_exc()
        log.error(exc)
        if _settings.DEBUG:
            print exc
            return
        if request.is_ajax():
            return HttpResponse("error")
        if request.method == "POST":
            return HttpResponse("error")
        return HttpResponseRedirect('%s/404/' % _settings.TBKT_STUDENT_ENGLISH_ROOT)
