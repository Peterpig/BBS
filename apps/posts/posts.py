# -*- coding: utf-8 -*-
import datetime
import logging
import markdown

from django.shortcuts import render_to_response

log = logging.getLogger(__name__)

def index(request, id):
    try:
        context = {}
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_to_response('posts/index.html', context)