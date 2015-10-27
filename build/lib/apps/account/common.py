# -*- coding: utf-8 -*-
import logging
import datetime,calendar
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context

def render_template(request, template_path, extra_context = {}):
    c = RequestContext(request)
    c.update(extra_context)
    return render_to_response(template_path, context_instance=c)

class Struct(dict):
    """
    - 为字典加上点语法. 例如:
    >>> o = Struct({'a':1})
    >>> o.a
    >>> 1
    >>> o.b
    >>> None
    """
    def __init__(self, dictobj={}):
        self.update(dictobj)

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val

    def __hash__(self):
        return id(self)