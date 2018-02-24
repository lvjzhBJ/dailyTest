# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import sys,os
import time
import pickle
from django import forms
from PIL import Image
from django.shortcuts import render,render_to_response,HttpResponse,redirect
from userAuth.models import User
from pageGet.models import Project,PageGet,ResponsePjt,ResponsePage,ResponseRpt
from images2gif import writeGif
from django.views.decorators.csrf import csrf_exempt
from userAuth.utils.time2json import CJsonEncoder

reload(sys)

sys.setdefaultencoding('utf8')


class ProjectNewForm(forms.Form):
    pjt_name = forms.CharField(required=True,
                               label='项目名称',
                               max_length=20
                               ,widget=forms.TextInput(attrs={
                                        'type': 'text',
                                       'class':'layui-input',
                                       'lay-verify':'required'}))


class ProjectForm(forms.Form):
    pjt_name = forms.CharField(required=True,
                               label='项目名称',
                               max_length=20
                               ,widget=forms.TextInput(attrs={
                                        'type': 'text',
                                       'class':'layui-input',
                                       'lay-verify':'required'}))

    apk_path = forms.CharField (required=True,
                                label='安装包'
                                ,widget=forms.TextInput(attrs={
                                        'id':       'oss_apk',
                                        'readonly': 'readonly',
                                        'type':      'text',
                                        'class':     'layui-input',
                                        'lay-verify':'required'}))


def get_tree(parent_pjt):
    pages = PageGet.objects.filter(parent=parent_pjt)
    sz = []
    for pg in pages:
        if pg.text != 'no_value':

            if ':id/' in pg.text:
                name = pg.text[pg.text.index('id'):]
            else:
                name = pg.text
        elif pg.resource_id != 'no_value':
            name = pg.resource_id[pg.resource_id.index('id'):]
        else:
            name = pg.bounds

        sz.append({"id": pg.id,
                   "name": name,
                   "text": pg.text,
                   "resource_id": pg.resource_id,
                   "x_class": pg.x_class,
                   "bounds": pg.bounds,
                   "is_run_error":pg.is_run_error,
                   "children": get_tree(pg.id)})

    return sz


def get_page_info(pr_id):

    pjt = PageGet.objects.filter(parent=None,x_class=pr_id)
    tree_view = []
    print pjt
    if pjt:
        for p_i in pjt:
            print '----',p_i.id
            tree_view.append({"id": p_i.id,
                              "name": p_i.text,
                              "spread":True,
                              "text":p_i.text,
                              "resource_id":p_i.resource_id,
                              "x_class":p_i.x_class,
                              "bounds":p_i.bounds,
                              "is_run_error": p_i.is_run_error,
                              "children": get_tree(p_i)})
    print tree_view
    return tree_view


@csrf_exempt
def page_get(request):
    print 'page_get'
    run_once = request.session.get('run_once', 0)
    pr_id = request.COOKIES.get('pr_id', None)
    print '-----',pr_id
    t = int(time.time()*1000) - int(run_once)

    if t>100 or not run_once:
        request.session['run_once'] = int(time.time()*1000)
        return HttpResponse('请先选择项目')

    if pr_id and pr_id != "-1":
        print 'run_once...'
        request.session['run_once'] = int(time.time())
        request.session['name'] = int(time.time())

        page_info = get_page_info(pr_id)
        print page_info
        return render_to_response('page_get.html',{'page_info':json.dumps(page_info)})
    return HttpResponse('请先选择项目2')


'''
user
'''


def db_insert_pjt(userid):

    user = User.objects.filter(id=userid)
    project_info = list(Project.objects.filter(pjt_owner=user).values('id','pjt_name','app_file','app_plate','pjt_owner','create_time','crom_status'))
    print project_info
    if project_info:
        pjt,is_new = ResponsePjt.objects.get_or_create(user_id=userid,
                                                       user_parent=user[0],
                                                       defaults={'pjt_info':pickle.dumps(project_info)})

        if not is_new:
            pjt.pjt_info=pickle.dumps(project_info)
            pjt.add_time = pjt.mod_time
            pjt.save()


def get_pjts(userid):
    pjt_list = ResponsePjt.objects.filter(user_id=userid)

    if len(pjt_list) == 1:
        return pickle.loads(pjt_list.values('pjt_info')[0]['pjt_info'])
    else:
        return None


@csrf_exempt
def user_show(request,un):
    username = request.session.get('username')
    ver_status=request.session.get ('ver_status')

    if un != username:
        request.session['ver_status'] = 'FAIL_用登录失效...'
        return redirect('/login')

    if request.method == 'GET':

        email = request.session.get('email')
        userid=request.session.get ('userid')

        project_info = get_pjts(userid)
        project_info_json = json.dumps(project_info,cls=CJsonEncoder)
        project_info_json = json.loads(project_info_json)
        request.session['project_info_json'] = project_info_json

        rsp = render(request, 'weHtml/user_show.html', {'username': username,
                                                        'email': email,
                                                        'ver_status':ver_status,
                                                        'project_info_json': project_info_json})

        return rsp


@csrf_exempt
def user_add(request,un):
    username = request.session.get('username')
    ver_status=request.session.get ('ver_status')

    if un != username:
        request.session['ver_status'] = 'FAIL_用登录失效...'
        return redirect('/login')

    if request.method == 'POST':
        projectform = ProjectNewForm(request.POST, request.FILES)

        if not projectform.is_valid():
            request.session['ver_status'] = 'FAIL_请输入项目名称...'
            return redirect('/' + username + '/show')

        pjt_name = projectform.cleaned_data['pjt_name']
        app_file = request.FILES.get('file', None)

        if not app_file:
            request.session['ver_status'] = 'FAIL_请选择安装包文件...'
            return redirect('/' + username + '/show')

        pjt = Project()
        pjt.pjt_name = pjt_name
        pjt.app_file = app_file
        userid = request.session.get('userid')
        user = User.objects.filter(username=username, id=userid)
        if not user:
            request.session['ver_status'] = 'FAIL_账户异常,请重新登录...'
            return redirect('/' + username + '/show')
        pjt.pjt_owner = user[0]
        if str(app_file)[-4:] == '.apk':
            pjt.app_plate = 'Android'
        pjt.save()

        db_insert_pjt(userid)

        request.session['ver_status'] = '项目' + pjt_name + '创建成功'
        return redirect('/' + username + '/show')
    else:
        projectform = ProjectNewForm()

        email = request.session.get('email')
        project_info_json = request.session.get('project_info_json')

        rsp = render(request, 'weHtml/user_add.html', {'username': username,
                                                       'email': email,
                                                       'ver_status':ver_status,
                                                       'projectform': projectform,
                                                       'project_info_json': project_info_json
                                                        })

        request.session['ver_status'] = None
        return rsp


@csrf_exempt
def user_new(request,un):
    username=request.session.get ('username')
    ver_status=request.session.get ('ver_status')

    if un!=username:
        request.session['ver_status']='FAIL_用登录失效...'
        return redirect ('/login')

    if request.method=='POST':
        projectform=ProjectForm(request.POST,request.FILES)

        if not projectform.is_valid ():
            request.session['ver_status']='FAIL_请输入项目名称...'
            return redirect ('/'+username+'/show')

        pjt_name=projectform.cleaned_data['pjt_name']
        # app_file=request.FILES.get ('file',None)

        # if not app_file:
        #     request.session['ver_status']='FAIL_请选择安装包文件...'
        #     return redirect ('/'+username+'/show')

        pjt=Project()
        pjt.pjt_name=pjt_name
        # pjt.app_file=app_file
        userid=request.session.get ('userid')
        user=User.objects.filter (username=username,id=userid)
        if not user:
            request.session['ver_status']='FAIL_账户异常,请重新登录...'
            return redirect ('/'+username+'/show')
        pjt.pjt_owner=user[0]
        # if str (app_file)[-4:]=='.apk':
        #     pjt.app_plate='Android'
        pjt.save ()

        db_insert_pjt(userid)

        request.session['ver_status']='项目'+pjt_name+'创建成功'
        return redirect ('/'+username+'/show')
    else:
        projectform=ProjectForm()

        email=request.session.get ('email')
        project_info_json=request.session.get('project_info_json')

        rsp=render (request,'weHtml/user_new.html',{'username':         username,
                                                    'email':            email,
                                                    'ver_status':       ver_status,
                                                    'projectform':      projectform,
                                                    'project_info_json':project_info_json
                                                    })

        request.session['ver_status']=None
        return rsp


@csrf_exempt
def user_del(request,un):
    username = request.session.get('username')
    ver_status=request.session.get ('ver_status')

    if un != username:
        request.session['ver_status'] = 'FAIL_用登录失效...'
        return redirect('/login')

    if request.method == 'GET':

        email = request.session.get('email')
        userid=request.session.get ('userid')

        project_info = get_pjts(userid)
        project_info_json=json.dumps (project_info,cls=CJsonEncoder)
        project_info_json = json.loads(project_info_json)

        request.session['project_info_json'] = project_info_json
        rsp = render(request, 'weHtml/user_del.html', {'username': username,
                                                       'email': email,
                                                       'ver_status':ver_status,
                                                       'project_info_json': project_info_json})
        return rsp


@csrf_exempt
def del_pjt(request,pjt):

    if request.method == 'GET':
        username = request.session.get('username')
        userid = request.session.get('userid')
        user = User.objects.filter(username=username, id=userid)

        if not user:
            request.session['ver_status'] = 'FAIL_用户失效,请重新登录...'
            return redirect('/' + username + '/del/')

        project_db_old = Project.objects.filter(pjt_owner=user[0],pjt_name = pjt)
        if not project_db_old:
            request.session['ver_status'] = 'FAIL_项目不存在,请重试...'
        else:
            PageGet.objects.filter(parent=None,x_class=project_db_old[0].id).delete()
        Project.objects.filter(pjt_owner=user[0], pjt_name=pjt).delete()
        ResponsePjt.objects.filter(user_parent=user[0], user_id=userid).delete()
        db_insert_pjt(userid)

        return redirect('/' + username + '/del')


'''
project
'''


def get_pages(pjt_id):
    page_tree = ResponsePage.objects.filter(pjt_id=pjt_id)

    if len(page_tree) == 1:
        return pickle.loads(page_tree.values('page_info')[0]['page_info'])
    else:
        return None

@csrf_exempt
def pjt_show(request,un,pjt):

    username = request.session.get('username')
    if un != username:
        request.session['ver_status'] = 'FAIL_用登录失效...'
        return redirect('/login')

    user_pjt = User.objects.filter(username=un)
    if not user_pjt:
        request.session['ver_status'] = '用户' + un + '已被删除...'
        return redirect('/login')

    pjt_on = Project.objects.filter(pjt_name=pjt,pjt_owner=user_pjt[0])

    if not pjt_on:
        request.session['ver_status'] = '项目' + pjt + '已被删除...'
        return redirect('/' + username)

    if request.method == 'GET':

        project_info_json = request.session.get('project_info_json')
        email = request.session.get('email')
        userid = request.session.get('userid')

        page_info = get_pages(pjt_on[0].id)
        page_info_json = json.dumps(page_info, cls=CJsonEncoder)
        request.session['page_info_json'] = page_info_json

        return render_to_response('weHtml/user_pjt_show.html',
                                  {'project_info_json':project_info_json,
                                   'userid': userid,
                                   'username':username,
                                   'email': email,
                                   'pjt':pjt,
                                   'pjt_id':pjt_on[0].id,
                                   'page_info':page_info_json})


@csrf_exempt
def pjt_edit(request,un,pjt):

    username = request.session.get('username')
    if un != username:
        return redirect('/login')

    user_pjt = User.objects.filter(username=un)
    if not user_pjt:
        request.session['ver_status'] = '用户' + un + '已被删除...'
        return redirect('/login')

    pjt_on = Project.objects.filter(pjt_name=pjt,pjt_owner=user_pjt[0])

    if not pjt_on:
        request.session['ver_status'] = '项目' + pjt + '已被删除...'
        return redirect('/' + username)

    if request.method == 'GET':

        project_info_json = request.session.get('project_info_json')
        email = request.session.get('email')
        userid = request.session.get('userid')

        page_info = get_pages(pjt_on[0].id)
        page_info_json = json.dumps(page_info, cls=CJsonEncoder)
        request.session['page_info_json'] = page_info_json

        return render_to_response('weHtml/user_pjt_edit.html',
                                    {'project_info_json':project_info_json,
                                       'email':email,
                                       'username':username,
                                       'pjt':pjt,
                                       'pjt_id':pjt_on[0].id,
                                       'userid':userid,
                                       'page_info':json.dumps(page_info)})


@csrf_exempt
def pjt_case(request,un,pjt):

    username = request.session.get('username')
    if un != username:
        return redirect('/login')

    user_pjt = User.objects.filter(username=un)
    if not user_pjt:
        request.session['ver_status'] = '用户' + un + '已被删除...'
        return redirect('/login')

    pjt_on = Project.objects.filter(pjt_name=pjt,pjt_owner=user_pjt[0])

    if not pjt_on:
        request.session['ver_status'] = '项目' + pjt + '已被删除...'
        return redirect('/' + username)

    if request.method == 'GET':

        project_info_json = request.session.get('project_info_json')
        email = request.session.get('email')
        userid = request.session.get('userid')

        page_info = get_pages(pjt_on[0].id)
        print page_info
        case_list=[]
        case_info=[]

        def get_case(child_info):
            for i in child_info:
                step={}
                if isinstance(i,dict):
                    if ':id/' in i['resource_id']:
                        step['resource_id']=i['resource_id'][i['resource_id'].index(':id/')+4:]
                    else:
                        step['resource_id'] = i['resource_id']
                    step['text']=i['text']
                    step['is_run_error']=i['is_run_error']
                    case_info.append(step)
                    if len(i['children'])>0:
                        get_case(i['children'])
                    else:
                        case_list.append(case_info)

        get_case(page_info)
        print case_list

        case_list_json = json.dumps(case_list, cls=CJsonEncoder)
        case_list_json = json.loads(case_list_json)

        request.session['case_list_json'] = case_list_json

        return render_to_response('weHtml/user_pjt_case.html',
                                        {'project_info_json':project_info_json,
                                       'email':email,
                                       'username':username,
                                       'pjt':pjt,
                                       'pjt_id':pjt_on[0].id,
                                       'userid':userid,
                                       'case_list_json':case_list_json})


'''
report
'''


@csrf_exempt
def rpt_show(request,un,pjt):
    username = request.session.get('username')

    project_info_json = request.session.get('project_info_json')
    email = request.session.get('email')
    userid = request.session.get('userid')

    pjt_on = Project.objects.filter(pjt_name=pjt)
    # rpt = ResponseRpt.objects.filter(pjt_id=pjt_on[0].id)

    # test_case_info = {}
    # test_case_info['status'] = 0
    # if rpt:
    #     test_case_info['status'] = 1
    #     test_case_info['test_case_list'] = pickle.loads(rpt[0].rpt_info)

    test_case_data = [[90, "#2dc6c8", "Pass"], [5, "#d7797f", "Fail"], [0, "#5ab1ee", "Block"], [5, "#b6a2dd", "NA"]]

    rsp = render(request, 'weHtml/rpt_show.html', {'username': username,
                                                   'email': email,
                                                   'pjt': pjt,
                                                   'rpt':'报告',
                                                   'pjt_id':pjt_on[0].id,
                                                   'userid':userid,
                                                   'test_case_data': json.dumps(test_case_data),
                                                   'project_info_json': project_info_json})
    return rsp


@csrf_exempt
def rpt_sum(request,un,pjt):
    username = request.session.get('username')

    project_info_json = request.session.get('project_info_json')
    email = request.session.get('email')
    userid = request.session.get('userid')

    pjt_on = Project.objects.filter(pjt_name=pjt)
    rpt = ResponseRpt.objects.filter(pjt_id=pjt_on[0].id)

    test_case_info={}
    test_case_info['status'] = 0
    if rpt:
        test_case_info['status'] = 1
        test_case_info['test_case_list'] = pickle.loads(rpt[0].rpt_info)

    rsp = render(request, 'weHtml/rpt_sum.html', {'username': username,
                                              'email': email,
                                              'pjt': pjt,
                                              'rpt':'报告',
                                              'pjt_id':pjt_on[0].id,
                                              'userid':userid,
                                              'test_case_info': test_case_info,
                                              'project_info_json': project_info_json})
    return rsp


@csrf_exempt
def rpt_playback(request,un,pjt):
    username = request.session.get('username')

    project_info_json = request.session.get('project_info_json')
    email = request.session.get('email')
    userid = request.session.get('userid')

    pjt_on = Project.objects.filter(pjt_name=pjt)
    rpt = ResponseRpt.objects.filter(pjt_id=pjt_on[0].id)

    test_case_info={}
    test_case_info['status'] = 0
    if rpt:
        test_case_info['status'] = 1
        test_case_info['test_case_list'] = pickle.loads(rpt[0].rpt_info)

    rsp = render(request, 'weHtml/rpt_playback.html', {'username': username,
                                                       'email': email,
                                                       'pjt': pjt,
                                                       'rpt':'报告',
                                                       'pjt_id':pjt_on[0].id,
                                                       'userid':userid,
                                                       'test_case_info': test_case_info,
                                                       'project_info_json': project_info_json})
    return rsp

