#!/usr/bin/env python
#coding=utf-8
import urllib2
import simplejson as json
import logging, traceback, os

from django.core.cache import cache
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.conf import settings as _settings
from django.template import RequestContext, loader, Context

from libs.utils.common import Redirect

from libs.models.posts.model import Posts
from libs.models.account.model import UserProfile

log = logging.getLogger(__name__)

anonymous_urls = ['/site_media/', '/media/', '/theme_media/', '/upload_media/']

login_urls = ['/t/', '/new/', '/member/root/']

class ProfilUser(object):
    def __init__(self,user):
        self.user = user

    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user_power'):
            user = self.user
            up = UserProfile.objects.seek(user=user)
            if up:
                user.name = up.name
                user.header_img = up.header_img
            else:
                up = UserProfile(
                        user=user,
                        name=user.username,
                        header_img="/site_media/img/default.jpg"
                    )
                up.save()
                user.name = up.name
                user.header_img = up.header_img

            request._cached_user_power = user
        return request._cached_user_power

class AuthenticationMiddleware(object):

    def process_request(self, request):
        if not request.user.is_anonymous():
            # 非匿名用户增加权限
            request.__class__.user = ProfilUser(request.user)

        path = str(request.path)

        for obj in anonymous_urls:
            if path.startswith(obj):
                return
        user = request.user

        #需要登录访问
        if user.is_anonymous(): #未登陆跳转首页
            if path in login_urls:
                return HttpResponseRedirect('/login/?url=%s' % path)   #   ('%s/' % _settings.URLROOT)

        # 右侧热点文章
        self.get_top(request)

        # 右侧社区详情
        self.get_bbs_detail(request)

    def process_exception(self, request, exception):
        """
        功能说明:view函数抛出异常处理
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


    def get_top(self,request):
        user = request.user
        # 右侧今日热议
        url = 'http://api.duoshuo.com/sites/listTopThreads.json?short_name=zhuzh&range=daily'
        try:
            resp = urllib2.urlopen(url).read()
            resp = json.loads(resp)
        except urllib2.HTTPError, error:
            print "Cannot remove service instance!", error

        top_list = []
        try:
            for i, r in enumerate(resp['response']):
                if i <= 10:
                    temp = {'id':'' ,'title':'', 'url':'','post':''}
                    temp['id'] = r['url'].split('t')[-1].split('/')[1].split('/')[0]
                    post = Posts.objects.seek(pk=temp['id'])
                    header_img = post.get_user_header()
                    temp['post'] = post
                    temp['header_img'] = post.header_img = header_img
                    top_list.append(temp)
                else:
                    break
        except Exception, e:
            top_list = []
        user.top_list = top_list


    def get_bbs_detail(self, request):
        # 右侧社区详情

        if cache.get('all_user'):
            all_user = cache.get('all_user')
        else:
            all_user = User.objects.filter(pk__gt=0).count()
            cache.set('all_user', all_user, 60*60*6)

        if cache.get('all_posts'):
            all_posts = cache.get('all_posts')
        else:
            all_posts = Posts.objects.filter(pk__gt=0).count()
            cache.set('all_posts', all_posts, 60*60*6)

        request.all_user = all_user if all_user else ""
        request.all_posts = all_posts if all_posts else ""


