import logging
import re, datetime
from django import template
from django.template import Node, TemplateSyntaxError,  resolve_variable
from django.conf import settings as _settings
log = logging.getLogger(__name__)

register = template.Library()

def cut_title(value, args):
    try:
        sub_fix = '...'
        real_len = 0
        args = str(args)
        bits = args.split(' ')

        if len(bits) == 2:
            if bits[1] == '' or bits[1] == 'none':
                sub_fix = ''
            else:
                sub_fix = '...'
        cut_len = int(bits[0])
        ret_val = ""
        for s in value:
            if real_len >= cut_len:
                ret_val = ret_val+sub_fix
                break
            if not re.match("^[\u4E00-\u9FA5]+$", s):
                if real_len + 2 <= cut_len:
                    ret_val += s
                    real_len += 2
            else:
                if real_len + 1 <= cut_len:
                    ret_val += s
                    real_len += 1
        return ret_val
    except Exception, e:
        return value

register.filter('cut_title', cut_title)
