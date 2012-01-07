# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from django.conf import settings
from pyhs import Manager

from photos.models import Photo

def home(request):
    if request.user.is_authenticated():
        return render(request, 'home.html', {
            'photos': Photo.find_by_owner(request.user.id,
                limit=Photo.get_num_photos(request.user.id), offset=0)
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            # trochę okrutne warto potem scalić te tabele
            hs = Manager()
            hs.insert(settings.HS_DBNAME, 'owners',
                [('owner', new_user.id), ('num_photos', 0)])
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {
        'form': form,
    })
