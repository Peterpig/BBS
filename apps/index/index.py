# -*- coding: utf-8 -*-
import inspect
import logging

from django.shortcuts import render_to_response

log = logging.getLogger(__name__)

def index(request):
    try:
        context = {}
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_to_response('index/index.html', context)