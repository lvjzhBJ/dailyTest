# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.utils import timezone


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=50,unique=True,error_messages={'invalid': '格式错了.'})
    phone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'password','email','phone','is_active')


admin.site.register(User, UserAdmin)


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10, choices=(("register",u"注册"), ("forget",u"找回密码")))
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=timezone.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'email','send_type','send_time')

admin.site.register(EmailVerifyRecord, EmailVerifyAdmin)