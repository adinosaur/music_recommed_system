#coding=utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User    
from django.contrib import auth
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required 
from accounts.forms import LoginForm, RegistForm
from django.views.decorators.csrf import csrf_exempt
from mymusic.models import Song
from mymusic.models import Singer
from mymusic.pages_assistant import Page_Assistant
from models import UserMessage
from social_music.models import Attention

@csrf_exempt
def register(request):
    if request.method == 'GET':
        form = RegistForm()
        return render_to_response("register.html", RequestContext(request, {'form': form}))
    else:         
        form = RegistForm(request.POST)
        register_flag = True
        tips_message = ''

        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            password_again = request.POST.get('password_again', '')
            email = request.POST.get('email', '')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                tips_message = u'用户名已存在'
                register_flag = False

            if register_flag == True and password != password_again:
                tips_message = u'两次密码不一致'
                register_flag = False

            if register_flag:
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email)   
                user.save()
                
                usermessage = UserMessage()
                
                print type(request.user)
                usermessage.user = user
                usermessage.save()
                return HttpResponseRedirect('/accounts/login/')
            
        return render_to_response(
            'register.html',
            RequestContext(request, {'form': form,
                                     'tips': True,
                                     'tips_title': u'错误!',
                                     'tips_message': tips_message}))


@csrf_exempt
def login(request): 
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/index/')
    else:
        if request.method == 'GET':  
            form = LoginForm()
            return render_to_response('login.html', RequestContext(request, {'form': form}))
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = auth.authenticate(username=username, password=password)

                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/accounts/index/')

            return render_to_response(
                'login.html',
                RequestContext(request, {'form': form,
                                         'tips': True,
                                         'tips_title': u'错误!',
                                         'tips_message': u'用户名或密码错误'}))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/')


@login_required
def index(request):

    if request.method == 'GET':
        p = request.GET.get('p', 1)

        #将网页分页展示
        page_assistant = Page_Assistant(count=Song.objects.count(), page_size=20)
        pre_page = page_assistant.get_pre_page_no(int(p))
        cur_page = int(p)
        nex_page = page_assistant.get_nex_page_no(int(p))
        page_nums = page_assistant.get_pages_list(cur_page)
        b, e = page_assistant.get_objects_by_pageno(cur_page)
        songs = Song.objects.all()[b:e]

        return render_to_response(
            'index.html', 
            RequestContext(request, {   'songs': songs,
                                        'user': request.user,
                                        'page_nums': page_nums,
                                        'pre_page': pre_page,
                                        'cur_page': cur_page,
                                        'nex_page': nex_page}))   

@login_required
def home(request):
    #访问个人主页
    if request.method == 'GET':
        id = request.GET['id']
        user = User.objects.get(pk=id)
        print "[INFO]accounts.views.home: (uid=%s, uname=%s)" %(id, user)
        try:
            usermessage = UserMessage.objects.get(user=user)
        except UserMessage.DoesNotExist:
            print "[ERROE]accounts.views.home: 内部错误,不存在的UserMessage"

        try:
            Attention.objects.get(user=request.user, attendedUser=user)
            isFollow = True
        except Attention.DoesNotExist:
            isFollow = False

        return render_to_response(
                'home.html', 
                RequestContext(request, {   'isFollow': isFollow,
                                            'theuser': user,
                                            'head': usermessage.head,
                                            'intro': usermessage.intro}))
