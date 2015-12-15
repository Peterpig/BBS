# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.db import models
from django.contrib.auth.models import User

from libs.models.catalog.model import Catalog
from libs.models.account.model import UserProfile

class Posts(models.Model):
    """用户发表帖子类"""
    title = models.CharField(u'文章标题', max_length=500)
    user = models.ForeignKey(User)
    type = models.IntegerField(u'类型', default=1)
    views = models.IntegerField(u'点击量', default=0)
    content = models.CharField(u'内容')
    add_time = models.DateField(u'添加时间')
    catalog = models.ForeignKey(Catalog)    # 分类
    end_date = models.DateField(u'投票截止日期') # type=2时有效

    class Meta:
        db_table = 'posts'

    def get_user_header(self):
        if UserProfile.objects.seek(user=self.user):
            return UserProfile.objects.seek(user=self.user).header_img
        else:
            return '/site_media/img/default.jpg'

    def get_posts_vote(self, date):
        # 该帖子的所有投票数
        option_list = Options.objects.filter(posts=self)
        if option_list:
            num = 0
            for o in option_list:
                if date:
                    num += o.get_count(date)
                else:
                    num += o.get_count()
            return num
        else:
            return 0

    def get_most_posts_vote(self):
        today = datetime.date.today()
        all_post = Posts.objects.filter(pk__gt=0)
        obj = ''    # 今天投票最多的文章
        for p in all_post:
            if not obj:
                obj = p
                continue
            else:
                num1 = obj.get_posts_vote(today)
                num2 = p.get_posts_vote(today)
                obj = obj if num1 < num2 else p
        return obj
class Options(models.Model):
    """帖子投票选项"""
    posts = models.ForeignKey(Posts)
    content = models.CharField(u'内容')
    img = models.CharField(u'投票图片')

    class Meta:
        db_table = 'posts_options'

    def get_count(self, date=''):
        obj = Vote.objects.filter(option=self)
        if date:
            obj = obj.filter(add_time__gt=date)
        return obj.count() if obj else 0

class Vote(models.Model):
    """帖子投票"""
    option = models.ForeignKey(Options)
    user_id = models.IntegerField(u'用户id', default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vote'

    def get_posts(self):
        return self.option.posts

# class Catalog(models.Model):
#     """文章分类"""
#     name = models.CharField(u'分类名称', max_length=500)

#     class Meta:
#         db_table = 'catalog'
