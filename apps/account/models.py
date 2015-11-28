#coding=utf8
from django.contrib.auth.models import User
from django.db import models

class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')

        parents = [b for b in bases if isinstance(b, ProfileBase)]

        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            #UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            #UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)

class ProfileUser(object):
    __metaclass__ = ProfileBase

class MyProfile(ProfileUser):
    phone_number = models.CharField(max_length=11)              # 手机号
    # data_power = models.IntegerField(default=0)                # 数据权限，0、一般用户 1、省管理员 2、市管理员 3、县区管理员 4、学校管理员
    logins = models.IntegerField(default=1)                    # 登录次数
    money = models.IntegerField(u'用户金币')                    # 金币
    ip = models.CharField(u'最后登陆ip')                        # 最后登陆ip
