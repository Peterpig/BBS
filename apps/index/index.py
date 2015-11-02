# -*- coding: utf-8 -*-
import inspect
import logging

from apps.account.common import render_template, Struct

from libs.models.posts.model import Posts 

log = logging.getLogger(__name__)

def index(request):
    """首页"""
    context = Struct()
    user = request.user
    try:
        posts_list = Posts.objects.filter(pk__gt=0)
        context['posts_list'] = posts_list
    except Exception, e:
        print e
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'index/index.html', context)


def wai_index(request):
    """外首页"""
    context = Struct()
    user = request.user
    try:
        pass
    except Exception, e:
        raise e

    return render_template(request, 'index/wai_index.html', context)