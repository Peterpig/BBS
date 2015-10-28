# -*- coding: utf-8 -*-
import datetime
import logging
import markdown

from apps.account.common import render_template

from libs.models.posts.model import NewArticle

log = logging.getLogger(__name__)

def index(request, id):
    """文章首页"""
    try:
        context = {}
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/index.html', context)


def new(request):
    """发表文章"""
    try:
        context = {}
        form = NewArticle()
        context['form'] = form
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/new.html', context)