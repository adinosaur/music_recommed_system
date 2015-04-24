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

@csrf_exempt
def register(request):
    if request.method == 'GET':
        form = RegistForm()
        return render_to_response("register.html", {
            'form': form,
        })
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
    songs = Song.objects.all()
    print len(songs)
    return render_to_response('index.html', RequestContext(request, {'songs': songs}))