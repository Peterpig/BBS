# -*- coding: utf-8 -*-
import inspect
import logging
import random

import urllib2
import simplejson as json

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
        top_view = Posts.objects.filter(pk__gt=0, type=2).order_by('-views')[:5]
        # 最新发布的榜单
        top_new = Posts.objects.filter(pk__gt=0, type=2).order_by('-add_time')[:5]
        # 最后投票的榜单
        top_vote = Vote.objects.filter(pk__gt=0, option__posts__type=2).order_by('-add_time')[:5]
        context.top_view = top_view
        context.top_new = top_new
        context.top_vote = top_vote

        ########### 话题 ###########

        # 最热榜单
        top_view_2 = Posts.objects.filter(pk__gt=0, type=1).order_by('-views')[:5]
        # 最新发布的榜单
        top_new_2 = Posts.objects.filter(pk__gt=0, type=1).order_by('-add_time')[:5]
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

        ########### s2 ###########
        s2 = request.session.get('top_list', '')
        if s2:
            s2 = s2[0]
            id = s2['id']
            s2_post = Posts.objects.seek(pk=id)
            s2_option = Options.objects.filter(posts=s2_post)
            s2['post'] = s2_post
            s2['option'] = s2_option
        context.catalog_list = catalog_list
        context.top_view_2 = top_view_2
        context.s2 = s2
        # context.top_top_2 = request.top_list
    except Exception, e:
        print e
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
