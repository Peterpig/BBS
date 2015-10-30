# -*- coding: utf-8 -*-
import datetime
import logging

from django.http import HttpResponse

from apps.account.common import render_template, Struct

from libs.models.posts.model import Posts
from libs.utils.ajax import ajax_ok, ajax_fail

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
            title = request.POST.get('title')
            content = request.POST.get('content')
            tag = request.POST.get('tag')
            type = request.POST.get('type', 1)

            if not title:
                return ajax_fail('文章标题不能为空')

            if not tag:
                return ajax_fail('请选择一个分类！')

            posts = Posts(
                    title = title,
                    user = user,
                    content = content,
                    add_time = datetime.datetime.now(),
                    type = type,
                    tag = tag
                )
            # posts.save()
            return ajax_ok(posts.id)
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/new.html', context)