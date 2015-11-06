# -*- coding: utf-8 -*-
import datetime
import inspect
import logging

import simplejson as json

from django.http import HttpResponse

from apps.account.common import render_template, Struct
from libs.utils.ajax import ajax_ok, ajax_fail

from libs.models.posts.model import Posts, Options
from libs.models.catalog.model import Catalog

log = logging.getLogger(__name__)

def index(request, id):
    """文章首页"""
    try:
        context = Struct()
        try:
            id = int(id)
        except Exception, e:
            return HttpResponse("/")
        posts = Posts.objects.seek(pk=id)
        context.posts = posts
    except Exception, e:
        print e
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/index.html', context)


def new(request):
    """发表文章"""
    try:
        context = {}
        if request.method == "POST":
            user = request.user
            data_dict = request.POST.get('data_dict')
            # title = request.POST.get('title')
            # content = request.POST.get('content')
            # tag = request.POST.get('tag')
            # type = int(request.POST.get('type', 1))

            data_dict = json.loads(data_dict)
            print "data_dict == ",data_dict
            print "*"*15
            print "title == ",data_dict['title']
            print "content == ",data_dict['content']
            print "tag == ",data_dict['tag']
            print "type == ",data_dict['type']
            print "*"*15

            if not data_dict['title']:
                return ajax_fail('文章标题不能为空')

            if not data_dict['tag']:
                return ajax_fail('请选择一个分类！')

            if type == 1:
                # 评论
                posts = Posts(
                        title = data_dict['title'],
                        user = user,
                        content = data_dict['content'],
                        add_time = datetime.datetime.now(),
                        type = data_dict['type'],
                        catalog__id = data_dict['tag']
                    )
            else:
                # 投票
                p = Posts(
                    title = data_dict['title'],
                    user = user,
                    add_time = datetime.datetime.now(),
                    type = data_dict['type'],
                    catalog_id = data_dict['tag']
                    )
                print "p === ",p.id, p.title
                p.save()
                # 添加选项内容
                option_list = data_dict['option']
                for option in option_list:
                    o = Options(
                            posts = p,
                            content = option
                        )
                    print "o === ",o
                    o.save()
            return ajax_ok(p.id)

        # GET
        catalog_list = Catalog.objects.filter(pk__gt=0)
        print "catalog_list == ",catalog_list
        context['catalog_list'] = catalog_list
    except Exception, e:
        print e
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/new.html', context)