# -*- coding: utf-8 -*-
import inspect
import logging
import random

from apps.account.common import render_template, Struct
from libs.utils.lib_page import Page

from libs.models.posts.model import Posts

log = logging.getLogger(__name__)

def index(request):
    """首页"""
    context = Struct()
    user = request.user
    try:
        page_no = request.REQUEST.get('p', 1)
        posts_list = Posts.objects.filter(pk__gt=0).order_by('-add_time')
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
        top_view = Posts.objects.filter(pk__gt=0).order_by('-views')
        # 最新发布的榜单
        top_new = Posts.objects.filter(pk__gt=0).order_by('-add_time')
        # 最后投票的榜单
        # top_vote = Posts.objects.filter(pk__gt=0).order_by('last_vote_time')
        context.catalog_list = catalog_list
    except Exception, e:
        print e

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
