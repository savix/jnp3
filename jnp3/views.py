# -*- coding: utf-8 -*-

import re

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.db import IntegrityError

from django.conf import settings
from pyhs import Manager

from users.models import User
from photos.models import Photo

def home(request):
    if request.user.is_authenticated():
        return render(request, 'home.html', {
            'photos': Photo.find_by_owner(request.user.id,
                limit=settings.PHOTOS_PER_PAGE, offset=0)
            #'photos': Photo.find_by_desc('sushi', 5, 0)[0]
        })
    else:
        return login(request)
    #return render_to_response('home.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form
    })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if not re.match(r'^\w{5,}$', username):
            error = 'invalid_username'
        elif len(password) < 5:
            error = 'invalid_password'
        elif password != password2:
            error = 'password_mismatch'
        else:
            try:
                User.create(username, password)
            except IntegrityError:
                error = 'username_taken'
            else:
                return HttpResponseRedirect("/")
    else:
        error = ''
        username = ''

    return render(request, "register.html", {
        'error': error,
        'username': username
    })
