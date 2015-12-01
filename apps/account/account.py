# -*- coding: utf-8 -*-
import datetime
import inspect
import logging

import simplejson as json

from django.http import HttpResponse
from django.conf import settings

from apps.account.common import render_template, Struct
from libs.utils.ajax import ajax_ok, ajax_fail

from libs.models.posts.model import Posts, Options, Vote
from libs.models.catalog.model import Catalog
from libs.models.account.model import UserProfile

log = logging.getLogger(__name__)

def user_index(request, name):
    """文章首页"""
    user = request.user
    context = {}
    try:
        context['UPLOAD_IMG_API'] = settings.UPLOAD_IMG_API
        context['IMG_START'] = settings.IMG_START
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'account/user_index.html', context)


def new(request):
    """发表文章"""
    try:
        context = {}
        if request.method == "POST":
            user = request.user
            data_dict = request.POST.get('data_dict')
            data_dict = json.loads(data_dict)

            if not data_dict['title']:
                return ajax_fail('文章标题不能为空')

            if not data_dict['tag']:
                return ajax_fail('请选择一个分类！')

            type = int(data_dict['type'])
            if type == 1:
                # 评论
                posts = Posts(
                        title = data_dict['title'],
                        user = user,
                        content = data_dict['content'],
                        add_time = datetime.datetime.now(),
                        type = data_dict['type'],
                        catalog__id = data_dict['tag']
                    )
                posts.save()
            else:
                # 投票
                p = Posts(
                    title = data_dict['title'],
                    user = user,
                    add_time = datetime.datetime.now(),
                    type = data_dict['type'],
                    catalog_id = data_dict['tag']
                    )
                p.save()
                # 添加选项内容
                option_list = data_dict['option']
                for option in option_list:
                    o = Options(
                            posts_id = p.id,
                            content = option['val'],
                            img = option['img']
                        )
                    o.save()

            return ajax_ok(p.id)

        # GET
        catalog_list = Catalog.objects.filter(pk__gt=0)
        context['catalog_list'] = catalog_list
        context['UPLOAD_IMG_API'] = settings.UPLOAD_IMG_API
        context['IMG_START'] = settings.IMG_START
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/new.html', context)


def change_header_img(request):
    """更换用户头像"""
    user = request.user
    ret_val = "err"
    try:
        if request.method == "POST":
            url = request.POST.get('url')
            user_profile = UserProfile.objects.filter(user=user)
            if url:
                if user_profile:
                    user_profile.update(
                        header_img=url
                        )
                    ret_val = "ok"
                else:
                    up = UserProfile(
                            user=user,
                            name=user.username,
                            header_img=url
                        )
                    up.save()
                    ret_val = "ok"
            else:
                ret_val = u"图片地址不存在！"
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return HttpResponse(ret_val)
