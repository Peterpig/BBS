# -*- coding: utf-8 -*-
import datetime
import inspect
import logging

import simplejson as json

from django.http import HttpResponse
from django.conf import settings

from apps.account.common import render_template, Struct
from libs.utils.ajax import ajax_ok, ajax_fail

from libs.models.account.model import UserProfile
from libs.models.posts.model import Posts, Options, Vote
from libs.models.catalog.model import Catalog

log = logging.getLogger(__name__)

def index(request, id):
    """文章首页"""
    user = request.user
    all_vote = 0
    option_list = ""
    try:
        context = Struct()
        try:
            id = int(id)
        except Exception, e:
            return HttpResponse("/")

        posts = Posts.objects.seek(pk=id)
        up = UserProfile.objects.seek(user=posts.user)
        posts.user.header_img = up.header_img if up else ""
        if posts.type == 2:
            option_list = Options.objects.filter(posts=posts)
            all_vote = Vote.objects.filter(option__in=option_list).count()
            for option in option_list:
                v_count = Vote.objects.filter(
                                option__id=option.id
                            ).count()

                # 每个选项的票数
                option.v_count = v_count

                # 每个选项的百分比
                option.present = int(float(v_count)/float(all_vote)) if all_vote else 0
        posts.views = posts.views + 1
        posts.save()
        context.posts = posts
        context.option_list = option_list
    except Exception, e:
        print e
        log.error("%s:%s" % (inspect.stack()[0][3], e))

    return render_template(request, 'posts/index.html', context)


def new(request):
    """发表文章"""
    try:
        context = {}
        if request.method == "POST":
            user = request.user
            data_dict = request.POST.get('data_dict')
            # title = request.POST.get('title')
            # content = request.POST.get('content')
            # tag = request.POST.get('tag')
            # type = int(request.POST.get('type', 1))

            data_dict = json.loads(data_dict)

            if not data_dict['title']:
                return ajax_fail('文章标题不能为空')

            if not data_dict['tag']:
                return ajax_fail('请选择一个分类！')

            type = int(data_dict['type'])

            print "data_dict['tag'] == ",data_dict['tag']
            print "data_dict['content'] == ",data_dict['content']
            if type == 1:

                if not Posts.objects.filter(title=data_dict['title']):
                    # 评论
                    p = Posts(
                            title = data_dict['title'],
                            user = user,
                            content = data_dict['content'],
                            add_time = datetime.datetime.now(),
                            type = data_dict['type'],
                            catalog_id = data_dict['tag']
                        )
                    p.save()
                else:
                    return ajax_fail(error="文章已存在,请换个标题试试!")
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


def post_vote(request):
    """POST投票按钮"""
    user = request.user
    try:
        if request.POST:
            option_id = request.POST.get('option_id')
            option = Options.objects.seek(pk=int(option_id))
            if not Vote.objects.filter(option=option, user_id=user.id):
                v = Vote(
                        option=option,
                        user_id=user.id,
                        add_time=datetime.datetime.now()
                    )
                v.save()
                num = Vote.objects.filter(option=option).count()
                return ajax_ok(data=num)
            else:
                return ajax_fail(error="您已经投过票了！")
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))
        return ajax_fail(error="系统异常！")


def post_vote_del(request):
    """POST投票删除按钮"""
    user = request.user
    try:
        if request.POST:
            option_id = request.POST.get('option_id')
            option = Options.objects.seek(pk=int(option_id)).delete()
            Vote.objects.filter(option__id=option_id).delete()
            return ajax_ok()
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))
        return ajax_fail(error="系统异常！")

def post_posts_del(request):
    """POST投票按钮"""
    user = request.user
    try:
        if request.POST:
            posts_id = request.POST.get('option_id')
            print "posts_id ==",posts_id
            Vote.objects.filter(option__posts__id=posts_id).delete()
            Options.objects.filter(posts__id=posts_id).delete()
            Posts.objects.filter(pk=posts_id).delete()
            return ajax_ok()
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))
        return ajax_fail(error="系统异常！")


def add_option(request):
    """POST添加选项"""
    try:
        if request.POST:
            data = request.POST.get('data')
            data = json.loads(data)

            option = Options(
                        posts_id=data['post_id'],
                        content=data['content'],
                        img=data['url']
                    )
            option.save()
            return ajax_ok(data='ok')
    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))
        return ajax_fail(error="系统异常！")
