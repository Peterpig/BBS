# -*- coding: utf-8 -*-
import inspect
import logging

from django.shortcuts import render_to_response

log = logging.getLogger(__name__)

def index(request):
    """首页"""
    context = {}
    try:
        num = [i for i in xrange(0,20)]
        print num
        context['num'] = num
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_to_response('index/index.html', context)


def login(request):
    """登陆界面"""
    context = {}
    try:
        pass
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_to_response('index/login.html', context)