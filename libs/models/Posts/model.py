# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from  DjangoUeditor.forms import UEditorField

class Posts(models.Model):
    """用户发表帖子类"""
    title = models.CharField(u'文章标题', max_length=500)
    user = models.ForeignKey(User)
    views = models.IntegerField(u'点击量')
    content = models.TextField(u'内容')
    add_time = models.DateField(u'添加时间', auto_now_add=True)

    class meta:
        db_table = 'posts'

class Message(models.Model):
    """帖子留言"""
    user_id = models.IntegerField(u'用户id', default=0)
    posts = models.ForeignKey(Posts)
    content = models.CharField(u'内容')
    message_to = models.IntegerField(u'@的人')

    class meta:
        db_table = 'message'


class NewArticle(forms.Form):
    Description=UEditorField("描述",initial="abc",width=600,height=800)