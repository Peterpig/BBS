# -*- coding: utf-8 -*-
from django import forms
from django.db import models

class Catalog(models.Model):
    """文章分类"""
    name = models.CharField(u'分类名称', max_length=500)

    class Meta:
        db_table = 'catalog'