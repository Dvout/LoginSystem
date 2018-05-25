from django.shortcuts import render
from django.shortcuts import redirect
from django.db import models
from .models import User
from . import forms
import hashlib
from django.core.exceptions import ValidationError
# Create your views here.


def index(request):
    pass
    return render(request, 'login/index.html')


def alterPwd(request):
    if request.method == "POST":
        AlterPwd_form = forms.AlterPwdForm(request.POST)
        re = AlterPwd_form.is_valid()
        if re:  # 获取数据
            AlterPwd_email = request.session['user_email']
            user = User.objects.get(email=AlterPwd_email)
            oldpassword = AlterPwd_form.cleaned_data['oldpassword']
            password1 = AlterPwd_form.cleaned_data['password1']
            password2 = AlterPwd_form.cleaned_data['password2']
            if user.password != hash_code(oldpassword):
                message = "旧密码错误"
                return render(request, 'login/alterPassword.html', locals())
            if  password1.isalnum() != True:
                message = "密码必须是字母和数字的组合,不能有符号！"
                return render(request, 'login/alterPassword.html', locals())
            if password1.isdigit() == True:
                message = "密码必须是字母和数字的组合，密码太过简单！"
                return render(request, 'login/alterPassword.html', locals())
            if password1.isalpha() == True:
                message = "密码必须是字母和数字的组合，密码太过简单！"
                return render(request, 'login/alterPassword.html', locals())
            if len(password1)<6 or len(password1)>18:
                message = "密码必须是6-18位"
                return render(request, 'login/alterPassword.html', locals())
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/alterPassword.html', locals())
            if password1 == oldpassword:
                message = "与旧密码相同！"
                return render(request, 'login/alterPassword.html', locals())
            #用户密码相同而且是处于登录状态 and request.session['is_login'] == True
            if user.password == hash_code(oldpassword):
                user.password = hash_code(password1)
                user.save()
                #直接退出重新登录
                #return redirect("/index/")
                request.session.flush()
                return redirect("/login/")
            else:
                message = "旧密码不正确！"
        else:
            return render(request, 'login/alterPassword.html', {'AlterPwd_form': AlterPwd_form})
    AlterPwd_form = forms.AlterPwdForm()
    return render(request, 'login/alterPassword.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
        # 刷新验证码

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        re = login_form.is_valid()
        if re:
            user_email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(email=user_email)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.email
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        else:
            return render(request, 'login/login.html', {'login_form': login_form})
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())




def hash_code(s, salt='SecondPro'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        #message = "请检查填写的内容！"
        re = register_form.is_valid()
        if re:  # 获取数据
            register_email = register_form.cleaned_data['email']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if  password1.isalnum() != True:
                message = "密码必须是字母和数字的组合,不能有符号！"
                return render(request, 'login/register.html')
            if password1.isdigit() == True:
                message = "密码必须是字母和数字的组合，密码太过简单！"
                return render(request, 'login/register.html', locals())
            if password1.isalpha() == True:
                message = "密码必须是字母和数字的组合，密码太过简单！"
                return render(request, 'login/register.html', locals())
            if len(password1)<6 or len(password1)>18:
                message = "密码必须是6-18位"
                return render(request, 'login/register.html', locals())
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_email_user = User.objects.filter(email=register_email)
                if same_email_user:  # 用户名唯一
                    message = '邮箱已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())

                        # 当一切都OK的情况下，创建新用户
                    new_user = User()
                    new_user.email = register_email
                    new_user.password = hash_code(password1)
                    new_user.save()
                    return redirect('/login/')  # 自动跳转到登录页面
        else:
            return render(request, 'login/register.html',{'register_form': register_form})
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html',locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")