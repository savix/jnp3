# -*- coding: utf-8 -*-

from os import path

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.shortcuts import HttpResponseRedirect

from tasks import prepare_photo_files
from models import Photo

from pymogile import Client, MogileFSError

def async_test_list(request):
    return render_to_response('async_test_list.html', {'photos': Photo.all()})

def async_test_add(request):
    photo = Photo.create('blablabla')
    prepare_photo_files.delay(photo.id)
    return HttpResponse('ok!')

def upload(request):
    storage = Client(domain = settings.MOGILEFS_DOMAIN,
            trackers = settings.MOGILEFS_TRACKERS)

    photo_file = request.FILES['photo']
    if photo_file.name.endswith('.jpg'):
        model = Photo.create(owner=request.user.id, desc=request.POST.get('desc'))
        #with open(path.join(settings.UNPROCESSED_PHOTOS_DIR, '%s.jpg' % model.id), 'wb') as f:
        with storage.new_file(path.join(settings.UNPROCESSED_PHOTOS_DIR,
                '%s.jpg' % model.id)) as f:
            for chunk in photo_file.chunks():
                f.write(chunk)
        f.close()
        prepare_photo_files(model.id) # .delay
        return HttpResponseRedirect('/')
