from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from datetime import datetime, timedelta, timezone
from .models import User
from .forms import LoginForm, RegisterForm
from django.conf import settings
import hashlib


def send_email(email, uid, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自MyBBS的注册确认邮件'

    text_content = '''感谢注册MyBBS！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册MyBBS，请点击下方的链接完成注册确认！\
                    </p>
                    <p><a href="http://{}/user/confirm/?uid={}&code={}" target=blank>点此确认注册</a></p>
                    '''.format('127.0.0.1:8000', uid, code)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def home(request):
    if request.session.get('uid', None):
        return render(request, 'user/home.html')
    else:
        return redirect('user:login')

def login(request):
    if request.session.get('uid', None):
        return redirect('bbs:index')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                if '@' in username:
                    user = User.objects.get(email=username)
                else:
                    user = User.objects.get(name=username)
            except Exception:
                message = '用户不存在！'
                return render(request, 'user/login.html', locals())

            if user.status == 0:
                message = '该用户还未经过邮件确认！'
                return render(request, 'user/login.html', locals())

            if user.password == hash_code(password):
                time = user.jointime.replace(tzinfo=timezone.utc)
                jointime = time.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
                request.session['uid'] = user.uid
                request.session['name'] = user.name
                request.session['avatar'] = str(user.avatar)
                request.session['email'] = user.email
                request.session['jointime'] = str(jointime)
                request.session['sp'] = user.sp
                request.session['level'] = user.level
                return redirect('bbs:index')
            else:
                message = '密码不正确！'
                return render(request, 'user/login.html', locals())

        else:
            return render(request, 'user/login.html', locals())

    else:
        login_form = LoginForm()
        return render(request, 'user/login.html', locals())

def logout(request):
    request.session.flush()
    return redirect('bbs:index')

def register(request):
    if request.session.get('uid', None):
        return redirect('bbs:index')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email')
            name = register_form.cleaned_data.get('name')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())
                same_name_user = User.objects.filter(name=name)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())

                user = User(sp=0, level=1, avatar='avatar/default.jpeg', status=0)
                user.email = email
                user.name = name
                user.password = hash_code(password1)
                user.jointime = datetime.now()
                user.save()
                
                code = hash_code(str(user.uid), name)
                send_email(email, str(user.uid), code)
                return redirect('user:login')
        return render(request, 'user/register.html', locals())
    else:
        register_form = RegisterForm()
        return render(request, 'user/register.html', locals())

def edit(request):
    uid = request.session.get('uid', None)
    if request.method == 'POST':
        u = User.objects.get(uid=uid)
        name = request.POST.get('name')
        u.name = name
        try:
            u.save()
        except Exception:
            return redirect('edit')
        request.session['name'] = name
        return render(request, 'user/edit.html')
    else:
        if uid:
            return render(request, 'user/edit.html')
        else:
            return redirect('user:login')

def upavatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('img')
        if avatar:
            uid = request.session.get('uid')
            u = User.objects.get(uid=uid)
            u.avatar = avatar
            u.save()
            request.session['avatar'] = 'avatar/' + str(avatar)

            content = {'avatar': request.session.get('avatar')}
            print(content)
            ret = JsonResponse(content)
            return HttpResponse(ret)
    else:
        return redirect('user:edit')

def user_confirm(request):
    uid = int(request.GET.get('uid', None))
    print(uid)
    code = request.GET.get('code', None)
    print(code)
    message = ''

    try:
        user = User.objects.get(uid=uid)
    except:
        message = '无效的确认请求！'
        return render(request, 'user/confirm.html', locals())

    if code == hash_code(str(uid), user.name):
        user.status = 1
        user.save()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'user/confirm.html', locals())
    else:
        message = '无效的确认请求！'
        return render(request, 'user/confirm.html', locals())

