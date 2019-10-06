from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "用户名/邮箱", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "密码"}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    email = forms.EmailField(label="电子邮箱", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "xxx@xxx.com"}))
    name = forms.CharField(label="用户名", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "用户名"}))
    password1 = forms.CharField(label="密码", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

    