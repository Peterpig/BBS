# -*- coding: utf-8 -*-
import datetime
import inspect
import logging
import random

import urllib2
import simplejson as json

from django.core.cache import cache
from django.db.models import Q
from django.conf import settings

from apps.account.common import render_template, Struct
from libs.utils.lib_page import Page

from libs.models.catalog.model import Catalog
from libs.models.posts.model import Posts, Vote, Options

log = logging.getLogger(__name__)

def index(request):
    """首页"""
    context = Struct()
    user = request.user
    try:
        page_no = request.REQUEST.get('p', 1)
        catalog_id = request.REQUEST.get('catalog', 0)
        posts_list = Posts.objects.filter(pk__gt=0).order_by('-add_time')

        if catalog_id:
            posts_list = posts_list.filter(catalog__id=catalog_id)
        page = Page(posts_list, request, pageno=page_no, paginate_by=20, )
        context['page'] = page

    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'index/index.html', context)


def wai_index(request):
    """外首页"""
    context = Struct()
    user = request.user
    try:
        catalog_list = get_tags()
        # 最热榜单
        top_view = Posts.objects.filter(pk__gt=0, type=2).order_by('-views')[:10]
        # 最新发布的榜单
        top_new = Posts.objects.filter(pk__gt=0, type=2).order_by('-add_time')[:10]
        # 最后投票的榜单
        top_vote = Vote.objects.filter(pk__gt=0, option__posts__type=2).order_by('-add_time')[:10]
        context.top_view = top_view
        context.top_new = top_new
        context.top_vote = top_vote

        ########### 话题 ###########

        # 最热榜单
        top_view_2 = Posts.objects.filter(pk__gt=0, type=1).order_by('-views')[:10]
        # 最新发布的榜单
        top_new_2 = Posts.objects.filter(pk__gt=0, type=1).order_by('-add_time')[:10]
        # 上升最快的榜单
        url = 'http://api.duoshuo.com/sites/listTopThreads.json?short_name=zhuzh&range=daily'
        try:
            resp = urllib2.urlopen(url).read()
            resp = json.loads(resp)
        except urllib2.HTTPError, error:
            top_top_2 = ''

        top_top_2 = []
        try:
            for i, r in enumerate(resp['response']):
                if i <= 1:
                    temp = {'id':'' ,'title':'', 'url':'','post':''}
                    temp['id'] = r['url'].split('t')[-1].split('/')[1].split('/')[0]
                    post = Posts.objects.seek(pk=temp['id'])
                    temp['post'] = post
                    top_top_2.append(temp)
                else:
                    break
        except Exception, e:
            top_top_2 = []

        ########### s2 今日最热投票 ###########
        today = datetime.date.today()
        all_vote_list = Vote.objects.filter(add_time__gt=today).order_by('option')
        _dic = {}
        for v in all_vote_list:
            if _dic.get(v.option.id):
                _dic[v.option.id].append(v.id)
            else:
                _list = []
                _list.append(v.id)
                _dic[v.option.id] = _list
        obj = ''
        num = 0
        for k in _dic:
            if not obj:
                obj = k
                num = len(_dic[k])
            else:
                num = num if num > len(_dic[k]) else len(_dic[k])
        if obj:
            op = Options.objects.seek(pk=obj)
            if op:
                obj = op.posts
                if obj.add_time >= datetime.datetime(today.year, today.month, today.day):
                    option_list = Options.objects.filter(posts=obj)
                    _list = []
                    for option in option_list:
                        v_count = Vote.objects.filter(option__id=option.id).count()

                        # 每个选项的票数
                        option.v_count = v_count
                        _list.append({'option':option, 'v_count':v_count})
                    option = sorted(_list, key=lambda x:-x['v_count'])
                    context.s2 = {'post':obj, 'option': option[:10]}
        context.catalog_list = catalog_list
        context.top_view_2 = top_view_2
        context.top_new_2 = top_new_2
        # context.top_top_2 = request.top_list
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))


    return render_template(request, 'index/wai_index.html', context)


def get_tags():
    """
    ---------------------------------------
    功能说明：标签云.随机生成不同颜色的标签
    ---------------------------------------
    """
    tags = Catalog.objects.all()
    tagscloud = []
    for obj in tags:
        size = random.randint(12, 30)   # 随机字体大小
        # 随机生成RGB
        R = random.randint(0, 254)
        G = random.randint(0, 254)
        B = random.randint(0, 254)
        RGB = 'rgb(%s,%s,%s)' % (R, G, B)

        dic = {}
        dic['name'] = obj.name
        dic['id'] = obj.id
        dic['size'] = size
        dic['rgb'] = RGB
        tagscloud.append(dic)
    return tagscloud


def search(request):
    """文章搜索"""
    context = {}
    try:
        kw = request.REQUEST.get('kw')
        posts_list = Posts.objects.filter(Q(title__contains=kw)|Q(content__contains=kw))
        page = Page(posts_list, request, pageno=1, paginate_by=20, )
        context['page'] = page
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'index/index.html', context)


def download_file(request): 
    """
    功能说明：    下载账号密码  
    """
    from django.http import HttpResponse
    port = request.GET.get("port","")
    password = request.GET.get("password","")
    s1 = request.REQUEST.get('s1', '')
    s2 = request.REQUEST.get('s2', '')
    response = HttpResponse(mimetype='text/plain')
    file_name = u"gui-config"
                                       
    response['Content-Disposition'] = 'attachment; filename=%s.json' % file_name.encode('GBK')
    
    if port and password and s1 and s2:
        response.write(u"""
            {
                "configs" : [
                    {
                        "remarks" : "",
                        "server" : "%s",
                        "server_port" : %s,
                        "password" : "%s",
                        "method" : "aes-256-cfb",
                        "obfs" : "plain",
                        "obfsparam" : "",
                        "remarks_base64" : "",
                        "tcp_over_udp" : false,
                        "udp_over_tcp" : false,
                        "protocol" : "origin",
                        "obfs_udp" : false,
                        "enable" : true,
                        "id" : "0E-25-50-5D-4F-C9-27-22-E7-1E-09-77-15-81-93-17"
                    },
                    {
                        "remarks" : "",
                        "server" : "%s",
                        "server_port" : %s,
                        "password" : "%s",
                        "method" : "aes-256-cfb",
                        "obfs" : "plain",
                        "obfsparam" : "",
                        "remarks_base64" : "",
                        "tcp_over_udp" : false,
                        "udp_over_tcp" : false,
                        "protocol" : "origin",
                        "obfs_udp" : false,
                        "enable" : true,
                        "id" : "0D-D0-62-25-64-AB-E1-6E-70-58-D7-6A-2A-B8-2E-B3"
                    }
                ],
                "index" : 0,
                "random" : false,
                "global" : false,
                "enabled" : true,
                "shareOverLan" : false,
                "isDefault" : false,
                "localPort" : 1080,
                "pacUrl" : "http://127.0.0.1:1080/pac",
                "useOnlinePac" : false,
                "reconnectTimes" : 3,
                "randomAlgorithm" : 0,
                "TTL" : 0,
                "proxyEnable" : false,
                "proxyType" : 0,
                "proxyHost" : null,
                "proxyPort" : 0,
                "proxyAuthUser" : null,
                "proxyAuthPass" : null,
                "autoban" : false
            }
        """% (s1, port, password, s2, port, password)
        )
    return response