# -*- coding: utf-8 -*-
import logging
import datetime
import inspect

from django.shortcuts import render_to_response

from django.contrib.auth.models import User

log = logging.getLogger(__name__)

def signup(request):
    try:
        context = {}
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_to_response('account/sinup.html', context)
        