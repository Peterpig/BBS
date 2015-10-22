# -*- coding: utf-8 -*-
import datetime
import logging
import markdown

from apps.account.common import render_template

log = logging.getLogger(__name__)

def index(request, id):
    try:
        context = {}
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/index.html', context)