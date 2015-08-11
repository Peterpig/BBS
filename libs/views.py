# -*- coding: utf-8 -*-
import inspect
import logging
import datetime
from django.shortcuts import render_to_response

def test(request):
    try:
        pass
    except Exception, e:
        raise e

    return render_to_response('1.html', {'current':datetime.datetime.now()})