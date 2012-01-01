# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response

from tasks import prepare_photo_files
from models import Photo

def async_test_list(request):
    return render_to_response('async_test_list.html', {'photos': Photo.all()})

def async_test_add(request):
    photo = Photo.create('blablabla')
    prepare_photo_files.delay(photo.id)
    return HttpResponse('ok!')
