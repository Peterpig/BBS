#coding=utf-8
import time
import logging

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
        else:
            print "aaaa"
    except Exception, e:
        print e
        log.error("%s:%s" % (inspect.stack()[0][3], e))

def resetpass(request):
    context = {}
    is_ok = 0   # 0未修改成功 1修改成功
    try:
        user = request.user
        form = ChangepwdForm()
        if request.method == 'POST':
            form = ChangepwdForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                oldpass = form.cleaned_data['oldpassword']
                pass1 = form.cleaned_data['newpassword1']
                pass2 = form.cleaned_data['newpassword2']
                user = authenticate(username=username, password=oldpass)
                if user is not None:
                    if user.is_active:
                        if pass1 != pass2:
                            form.add_error('newpassword2', u'两次密码不一致！')
                        else:
                            user.set_password(pass2)
                            user.save()
                            context['is_ok'] = 1
                            logout(request)
                    else:
                        form.add_error('username', u'用户被禁用，请联系管理员！')
                else:
                    form.add_error('oldpassword', u'账号或密码错误！')
        else:
            form = ChangepwdForm()
        context['form'] = form
    except Exception, e:
        return HttpResponse('err')
    return render_template(request, 'account/reset_password.html', context)
