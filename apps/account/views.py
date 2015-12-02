#coding=utf-8
import time
import logging
import simplejson as json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from apps.account.common import render_template

log = logging.getLogger(__name__)

def login_(request):
    try:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            u = authenticate(username=username, password=password)
            if u is not None:
                if u.is_active:
                    login(request, u)
                    request.session.set_expiry(0)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('not_active')
            else:
                return  HttpResponse('account_err')
    except Exception, e:
        return HttpResponse('err')

    return render_template(request, 'account/login.html', context)


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if username == '' or email == '' or password == '' or password2 == '':
                return HttpResponse('empty')

            try:
                if email.split('@')[0] == email:
                    return HttpResponse('email')
            except Exception, e:
                return HttpResponse('err')

            if password != password2:
                return HttpResponse('password_not_same')

            user_test = User.objects.filter(username=username)
            if user_test:
                return HttpResponse('exact')
            user = User.objects.create_user(username, email, password2)
            return HttpResponse('ok')

    except Exception, e:
        log.error("%s:%s" % (inspect.stack()[0][3], e))

def resetpass(request):
    context = {}
    is_ok = 0   # 0未修改成功 1修改成功
    try:
        user = request.user
        if request.method == 'POST':
            data = request.POST.get('data')
            data = json.loads(data)
            if data:
                oldpass = data['old']
                new1 = data['new1']
                new2 = data['new2']

                if not oldpass:
                    return HttpResponse(u"请输入旧密码！")
                if not new1:
                    return HttpResponse(u"请输入新密码！")
                if not new2:
                    return HttpResponse(u"请再次输入新密码！")
                if new1 != new2:
                    return HttpResponse(u"两次密码不一致！")
                if len(new1) < 6:
                    return HttpResponse(u"密码不能少于6位！")
                if oldpass == new1:
                    return HttpResponse(u"新旧密码不能一致！")

                # 认证
                user = authenticate(username=user.username, password=oldpass)
                if user is not None:
                    if user.is_active:
                        user.set_password(new2)
                        user.save()
                        return HttpResponse('ok')
                    else:
                        return HttpResponse(u'用户被禁用，请联系管理员！')
                else:
                    return HttpResponse(u'密码错误！')

    except Exception, e:
        return HttpResponse('err')
