# -*- coding: utf-8 -*-
import inspect
import logging

from apps.account.common import render_template

log = logging.getLogger(__name__)

def index(request):
    """首页"""
    context = {}
    user = request.user
    try:
        num = [i for i in xrange(0,20)]
        context['num'] = num
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'index/index.html', context)
