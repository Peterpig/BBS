#!/usr/bin/env python
# coding: utf-8

import os
import sys

# 设置工作目录
sys_base_path = os.path.abspath(__file__)
sys.path.append(os.path.normpath(os.path.join(sys_base_path, '../..')))
print "sys.path == "sys.path,
# 将系统的编码设置为UTF8
reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()