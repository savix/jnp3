# -*- coding: utf-8 -*-

from os import path

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from tasks import prepare_photo_files
from models import Photo
from ..users.models import User

from pymogile import Client, MogileFSError

@login_required
def upload(request):
    storage = Client(domain = settings.MOGILEFS_DOMAIN,
            trackers = settings.MOGILEFS_TRACKERS)

    photo_file = request.FILES.get('photo')
    photo_desc = request.POST.get('desc', '')
    if photo_file is None or not photo_file.name.endswith('.jpg') or \
            photo_file.size > settings.MAX_PHOTO_SIZE:
        # Mamy błąd
        return HttpResponseRedirect('/')
    else:
        model = Photo.create(owner=request.user.id, desc=photo_desc)
        #with open(path.join(settings.UNPROCESSED_PHOTOS_DIR, '%s.jpg' % model.id), 'wb') as f:
        with storage.new_file(path.join(settings.UNPROCESSED_PHOTOS_DIR,
                '%s.jpg' % model.id)) as f:
            for chunk in photo_file.chunks():
                f.write(chunk)
        f.close()
        prepare_photo_files.delay(model.id)
        return HttpResponseRedirect('/')

def gallery(request, username, page):
    try:
        limit = settings.PHOTOS_PER_PAGE
        offset = (int(page) - 1) * limit
        owner = User.get_by_username(username)
        photos = Photo.find_by_owner(owner.id, limit=limit, offset=offset)
        return render(request, 'gallery.html', {
            'owner': owner,
            'photos': photos
        })
    except User.DoesNotExist:
        return HttpResponseRedirect('/')


def photo(request, id):
    try:
        photo = Photo.get(id)
        owner = User.get(photo.owner)
        return render(request, 'photo.html', {
            'owner': owner,
            'photo': photo
        })
    except Photo.DoesNotExist, User.DoesNotExist:
        return HttpResponseRedirect('/')

def search(request):
    query = request.GET.get('q', '').strip()
    if query:
        photos, _ = Photo.find_by_desc(query, 30, 0)
    else:
        photos = None
    return render(request, 'search.html', {
        'query': query,
        'photos': photos
    })
