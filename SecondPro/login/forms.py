from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    email = forms.EmailField(label="邮箱", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}),
                             error_messages = {'required': '邮箱不能为空.', 'invalid': "邮箱格式错误"})
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',error_messages={'invalid':"验证码错误"})

class RegisterForm(forms.Form):
    email = forms.EmailField(label="邮箱", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}),
                             error_messages={'required': '邮箱不能为空.','invalid':"邮箱格式错误"})
    # "密码必须是字母和数字的组合,不能有符号！"
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                error_messages={'required': '邮箱不能为空.', 'invalid': "邮箱格式错误"})
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',error_messages={'invalid':"验证码错误"})


class AlterPwdForm(forms.Form):
    oldpassword = forms.CharField(label="旧密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',error_messages={'invalid':"验证码错误"})
