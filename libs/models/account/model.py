# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """文章分类"""
    user = models.ForeignKey(User)
    name = models.CharField(u'姓名', max_length=500)
    header_img = models.CharField(u'头像', max_length=500)

    class Meta:
        db_table = 'user_profile'
