# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pageGet.models import Project,PageGet,ResponsePjt,ResponsePage,ResponseRpt
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.http import JsonResponse,FileResponse
# Create your views here.


@csrf_exempt
def pjt2client(request):
    if request.method == 'GET':
        pjt_on = Project.objects.filter(crom_status=0)[:1]
        if pjt_on:
            print pjt_on[0]
            pjt_dict = {'id':pjt_on[0].id,
                        'pjt_name':pjt_on[0].pjt_name,
                        'app_plate':pjt_on[0].app_plate,
                        'pjt_owner':pjt_on[0].pjt_owner.id}
            rsp = JsonResponse(pjt_dict, safe=False)
            return rsp

@csrf_exempt
def app2client(request,pjt_id):
    if request.method == 'GET':
        pjt_on = Project.objects.filter(id=pjt_id)[:1]
        the_file_name = pjt_on[0].app_file
        response = FileResponse(the_file_name)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

        return response
