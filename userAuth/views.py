# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import re,hashlib
import time
from django.shortcuts import HttpResponse,render_to_response,render,redirect
from django import forms
from models import User
from pageGet.models import Project
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from utils.email_send import send_register_email
from userAuth.models import EmailVerifyRecord
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# Create your views here.
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

class VerForm(forms.Form):
    vercode = forms.CharField(required=True,
                              label='人类验证',
                              help_text='请输入图片字符',
                              error_messages={"invalid": u"验证码错误"},
                              widget=forms.TextInput(attrs={'type': 'text',
                                                         'required lay-verify': 'captcha_1',
                                                         'class': 'layui-input',
                                                         'lay-verify': 'required'}))


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='邮箱',
                             help_text='请输入注册邮箱',
                             widget=forms.TextInput(attrs={'required lay-verify':'email',
                                       'class':'layui-input',
                                       'lay-verify':'required'}))


class RegForm(forms.Form):

    email = forms.EmailField(required=True,
                             label='邮箱',
                             help_text='将会成为您唯一的登入名',
                             widget=forms.TextInput(attrs={'required lay-verify':'email',
                                       'class':'layui-input',
                                       'lay-verify':'required'}))

    phone = forms.CharField(required=True,
                            validators=[mobile_validate, ],
                            label='手机',
                            widget=forms.TextInput(attrs={'required lay-verify':'phone',
                                       'class':'layui-input',
                                       'lay-verify':'required'}))

    username = forms.CharField(required=True,
                               label='昵称',
                               widget=forms.TextInput(attrs={'required lay-verify':'username',
                                       'class':'layui-input',
                                       'lay-verify':'required'}))

    password = forms.CharField(required=True,
                               label='密码',
                               help_text='输入6到16个字符',
                               min_length=6,
                               max_length=20,
                               widget=forms.TextInput(attrs={'type':'password',
                                        'required lay-verify':'password',
                                        'class':'layui-input',
                                        'lay-verify':'required'}))


class UserForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='邮箱',
                             widget=forms.TextInput(attrs={'required lay-verify':'email',
                                       'class':'layui-input',
                                       'lay-verify':'required'}))
    password = forms.CharField(required=True,
                               label='密码',
                               min_length=6,
                               max_length=20,
                               widget=forms.TextInput(attrs={'type':'password',
                                        'required lay-verify':'password',
                                        'class':'layui-input',
                                        'lay-verify':'required'}))

@csrf_exempt
def refresh_captcha(request):
    to_json_response = dict()
    to_json_response['status'] = 1
    to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
    to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])

    return HttpResponse(json.dumps(to_json_response), content_type='application/json')



@csrf_exempt
def regist(request):

    if request.method == 'POST':
        regform = RegForm(request.POST)
        ver_form = VerForm(request.POST)

        if regform.is_valid() and ver_form.is_valid():
            email = regform.cleaned_data['email']
            # phone = regform.cleaned_data['phone']
            # username = regform.cleaned_data['username']
            # password = regform.cleaned_data['password']
            resp_ver = ver_form.cleaned_data['vercode']
            hash_key = request.POST.get('captcha_0')
            vv = CaptchaStore.objects.filter(response=resp_ver.lower(), hashkey=hash_key)
            if vv:
                d_time = vv[0].expiration.replace(tzinfo=None)
                ans_time = time.mktime(d_time.timetuple())
                if int(time.time() - ans_time) > 0:
                    request.session['ver_status'] = '验证码已失效'
                    return redirect('/regist')
            else:
                request.session['ver_status'] = '验证码输入错误,请重试'
                return redirect('/regist')

            phone=regform.cleaned_data['phone']
            username=regform.cleaned_data['username']
            password=regform.cleaned_data['password']
            user,is_new = User.objects.get_or_create(username=username,password=password,email=email,phone=phone)
            if is_new:
                # send_register_email(email, "register")
                userform=UserForm()
                return render_to_response('weHtml/login.html', {'userform': userform})
            else:
                request.session['ver_status'] = '用户已存在'
                return redirect('/login')

    reg_form = RegForm()
    ver_form = VerForm()
    reg_key = CaptchaStore.generate_key()
    reg_url = captcha_image_url(reg_key)
    ver_status = request.session.get('ver_status')

    rsp = render_to_response('weHtml/reg.html',{'reg_form':reg_form,
                                                'ver_form':ver_form,
                                                'reg_url':reg_url,
                                                'reg_key':reg_key,
                                                'ver_status':ver_status})
    request.session['ver_status'] = None
    return rsp


@csrf_exempt
def forget(request):

    if request.method == 'POST':
        forget_form=ForgetForm(request.POST)
        ver_form = VerForm(request.POST)

        if forget_form.is_valid() and ver_form.is_valid():
            email = forget_form.cleaned_data['email']
            response = ver_form.cleaned_data['vercode']
            hash_key = request.POST.get('captcha_0')
            vv = CaptchaStore.objects.filter(response=response.lower(), hashkey=hash_key)
            if vv:
                d_time = vv[0].expiration.replace(tzinfo=None)
                ans_time = time.mktime(d_time.timetuple())
                print 'time_now::', time.time()
                print 'time_old::', d_time
                if int(time.time() - ans_time) > 0:
                    return HttpResponse('验证码已失效')
            else:
                return HttpResponse('验证码输入错误,请重试')
            user =User.objects.filter(email=email)
            if user:
                send_register_email(email, "forget")
                userform=UserForm()
                return render_to_response('weHtml/login.html', {'userform': userform})

    fg_form = ForgetForm()
    ver_form = VerForm()
    reg_key = CaptchaStore.generate_key()
    reg_url = captcha_image_url(reg_key)
    rsp = render_to_response('weHtml/forget.html',{'fg_form':fg_form,
                                                      'ver_form':ver_form,
                                                      'reg_url':reg_url,
                                                      'reg_key':reg_key})
    return rsp


@csrf_exempt
def logout(request):
    if request.session.get('userid'):
        del request.session['userid']
    if request.session.get('username'):
        del request.session['username']
    if request.session.get('email'):
        del request.session['email']
    if request.session.get('project_info'):
        del request.session['project_info']
    if request.session.get('ver_status'):
        del request.session['ver_status']
    return redirect('/index')


@csrf_exempt
def active_user(request, active_code):

    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            request.session['ver_status'] = '用户激活失败'
    else:
        request.session['ver_status'] = '用户激活成功'

    return redirect('/login')


'''
add cookis
'''
@csrf_exempt
def index(request):
    return render(request, 'weHtml/index.html')


@csrf_exempt
def login(request):
    ver_status = request.session.get('ver_status')

    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data['email']
            password = userform.cleaned_data['password']

            if ver_status:
                ver_form = VerForm(request.POST)
                if ver_form.is_valid():
                    resp_ver = ver_form.cleaned_data['vercode']
                    hash_key = request.POST.get('captcha_0')
                    vv = CaptchaStore.objects.filter(response=resp_ver.lower(), hashkey=hash_key)
                    if vv:
                        d_time = vv[0].expiration.replace(tzinfo=None)
                        ans_time = time.mktime(d_time.timetuple())
                        if int(time.time() - ans_time) > 0:
                            request.session['ver_status'] = '验证码已失效'
                            return redirect('/login')
                    else:
                        request.session['ver_status'] = '验证码输入错误,请重试'
                        return redirect('/login')
                else:
                    request.session['ver_status'] = '验证码输入错误,请重试'
                    return redirect('/login')

            user = User.objects.filter(email=email,password__exact=password)
            if user:
                if user[0].is_active:
                    request.session['ver_status'] = None
                    request.session['userid'] = user[0].id
                    request.session['username'] = user[0].username
                    request.session['email'] = email
                    return redirect('/'+user[0].username+'/show')
                else:
                    request.session['ver_status'] = '用户未激活'
                    return redirect('/login')
            else:
                request.session['ver_status'] = '用户名或密码错误,请重新登录'
                return redirect('/login')

    user_form = UserForm()
    rsp = render_to_response('weHtml/login.html', {'userform': user_form})
    if ver_status:
        ver_form = VerForm()
        hash_key = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hash_key)

        rsp = render_to_response('weHtml/login.html',{'userform':user_form,
                                                      'ver_form':ver_form,
                                                      'imgage_url':imgage_url,
                                                      'hash_key':hash_key,
                                                      'ver_status': ver_status})
    request.session['ver_status'] = None
    return rsp
