# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.core.files.base import ContentFile
import traceback
from pageGet.models import Project,ResponsePage,ResponseRpt
from userAuth.models import User
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
# Create your views here.


@csrf_exempt
def pjt2client(request):
    if request.method == 'GET':
        pjt_on = Project.objects.filter(crom_status=0)[:1]
        if pjt_on:
            print pjt_on[0]
            pjt_dict = {'id':pjt_on[0].id,
                        'pjt_name':pjt_on[0].pjt_name,
                        'app_file':str(pjt_on[0].app_file),
                        'app_plate':pjt_on[0].app_plate,
                        'pjt_owner':pjt_on[0].pjt_owner.id}
            rsp = JsonResponse(pjt_dict, safe=False)
            return rsp

@csrf_exempt
def client2json(request):
    if request.method == 'POST':
        try:
            get_json = request.POST
            pjt_parent = Project.objects.filter(id=int(get_json.get('pjt_id')))
            resPage,is_new_page = ResponsePage.objects.get_or_create(pjt_id = int(get_json.get('pjt_id')),
                                                                  pjt_name = get_json.get('pjt_name'),
                                                                  pjt_parent = pjt_parent[0],
                                                                  defaults = {'page_info': get_json.get('rpt_info')})
            resRpt,is_new_rpt = ResponseRpt.objects.get_or_create(pjt_id = int(get_json.get('pjt_id')),
                                                                  pjt_name = get_json.get('pjt_name'),
                                                                  pjt_parent = pjt_parent[0],
                                                                  defaults={'rpt_info': get_json.get('test_case_list')})
            if not is_new_page:
                resPage.page_info=get_json.get('rpt_info')
                resPage.save()
            if not is_new_rpt:
                resRpt.rpt_info = get_json.get('test_case_list')
                resRpt.save()
            return HttpResponse('client2json|ResponsePage:'+str(resPage.id) + ' | ResponseRpt'+ str(resRpt.id), content_type='application/json')
        except:
            return HttpResponse(traceback.format_exc(), content_type='application/json')


@csrf_exempt
def client2img(request):
    if request.method == 'POST':
        try:
            get_json = request.POST
            img_path = os.path.join(os.path.dirname(__file__)) \
                       + '/media/img/user' \
                       + str(get_json.get('pjt_parent')) \
                       + '/pjt' \
                       + str(get_json.get('pjt_id'))\
                       +'/'
            img_save_path = './img/user' \
                       + str(get_json.get('pjt_parent')) \
                       + '/pjt' \
                       + str(get_json.get('pjt_id'))\
                       +'/'
            keys = request.FILES.keys()
            print img_path
            for k in keys:
                app_file = request.FILES[k]
                if app_file:
                    if os.path.exists(img_path + k):
                        os.remove(img_path + k)
                    default_storage.save(img_save_path + k, ContentFile(app_file.read()))
            return HttpResponse('client2img|'+img_path+'|'+img_save_path+'|'+','.join(keys), content_type='application/json')
        except:
            return HttpResponse(traceback.format_exc(), content_type='application/json')


@csrf_exempt
def clean_apk(request):
    if request.method == 'POST':
        try:
            get_json = request.POST
            img_path = os.path.join(os.path.dirname(__file__)) + '/media/appfile/'
            pjt_id = get_json.get('pjt_id')
            pjt_owner = get_json.get('pjt_owner')
            app_file = get_json.get('app_file')

            po=User.objects.filter(id=pjt_owner)
            acc_pjt = Project.objects.filter(pjt_owner=po,id=pjt_id)
            exit_app=[]
            if acc_pjt:
                all_pjt = Project.objects.all()

                if all_pjt:
                    for i in all_pjt:
                        exit_app.append(i.app_file.name.replace('appfile/',''))

            all_app = os.listdir(img_path)

            for i in all_app:
                if i in exit_app:
                    print 'pjt apk is:',i
                else:
                    if os.path.exists(img_path+i):
                        print 'del apk:', img_path + i
                        # 删除文件，可使用以下两种方法。
                        os.remove(img_path+i)
                        # os.unlink(my_file)
                    else:
                        print 'no such file:%s' % img_path+i

            return HttpResponse(acc_pjt, content_type='application/json')
        except:
            return HttpResponse(traceback.format_exc(), content_type='application/json')
