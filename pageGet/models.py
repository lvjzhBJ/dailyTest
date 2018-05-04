# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from userAuth.models import User
from django.contrib import admin
from mptt.models import MPTTModel
from django.utils import timezone
# Create your models here.


class PageGet(MPTTModel):
    '''
    is_run_error:0未初始化、1ok、2、3、4没反馈、5link、
    '''
    id = models.AutoField(primary_key=True)
    bounds = models.CharField(max_length=512)
    resource_id = models.CharField(max_length=512,null=True)
    text = models.CharField(max_length=128,null=True)
    x_class = models.CharField(max_length=128)
    is_run_error = models.IntegerField(default=0)
    operation = models.CharField(max_length=64,null=True)
    link_node= models.IntegerField(default=0)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")

    class MPTTMeta:
        parent_attr = 'parent'

    def __unicode__(self):
        return str(self.id)


class PageGetAdmin(admin.ModelAdmin):
    list_display = ('id','parent','is_run_error','text','operation','resource_id', 'link_node','bounds','x_class')

admin.site.register(PageGet, PageGetAdmin)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    pjt_name = models.CharField(max_length=50)
    app_file = models.FileField(upload_to='appfile')
    app_plate = models.CharField(max_length=20)
    pjt_owner = models.ForeignKey(User)
    create_time = models.DateTimeField(default=timezone.now)
    crom_status = models.IntegerField(default=0)
    stand = models.IntegerField(default=0)

    def __unicode__(self):
        return  self.pjt_name


class ProjectnewAdmin(admin.ModelAdmin):
    list_display = ('id','pjt_name','app_file','app_plate','pjt_owner','create_time','crom_status','stand')


admin.site.register(Project, ProjectnewAdmin)


class ResponsePjt(models.Model):
    user_id = models.IntegerField(default=0)
    pjt_info = models.CharField(max_length=32768,null=True)
    add_time = models.DateTimeField('添加日期',default = timezone.now)
    mod_time = models.DateTimeField('更新日期',auto_now_add=True)
    user_parent = models.ForeignKey(User,default=None)


class ResponsePjtAdmin(admin.ModelAdmin):
    list_display = ('user_id','pjt_info','add_time','mod_time','user_parent')

admin.site.register(ResponsePjt, ResponsePjtAdmin)


class ResponsePage(models.Model):
    pjt_id = models.IntegerField(default=0)
    pjt_name = models.CharField(max_length=128,null=True)
    page_info = models.CharField(max_length=32768,null=True)
    add_time = models.DateTimeField('添加日期',default = timezone.now)
    mod_time = models.DateTimeField('更新日期',default = timezone.now)
    pjt_parent = models.ForeignKey(Project,default=None)


class ResponsePageAdmin(admin.ModelAdmin):
    list_display = ('id','pjt_id','pjt_name','add_time','mod_time','page_info','pjt_parent')

admin.site.register(ResponsePage, ResponsePageAdmin)


class ResponseRpt(models.Model):
    pjt_id = models.IntegerField(default=0)
    pjt_name = models.CharField(max_length=128,null=True)
    rpt_info = models.CharField(max_length=32768,null=True)
    add_time = models.DateTimeField('添加日期',default = timezone.now)
    mod_time = models.DateTimeField('更新日期',default = timezone.now)
    pjt_parent = models.ForeignKey(Project,default=None)


class ResponseRptAdmin(admin.ModelAdmin):
    list_display = ('pjt_id','pjt_name','add_time','mod_time','rpt_info','pjt_parent')

admin.site.register(ResponseRpt, ResponseRptAdmin)


class ManualCase(models.Model):
    pjt_id = models.IntegerField(default=0)
    case_info = models.CharField(max_length=32768,null=True)


class ManualCaseAdmin(admin.ModelAdmin):
    list_display = ('id','pjt_id','case_info')

admin.site.register(ManualCase, ManualCaseAdmin)

