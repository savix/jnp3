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
                '%s,%s.jpg' % (model.owner, model.nb))) as f:
            for chunk in photo_file.chunks():
                f.write(chunk)
        f.close()
        prepare_photo_files.delay(model.owner, model.nb)
        return HttpResponseRedirect('/')

def gallery(request, owner, page):
    try:
        page = int(page)
        limit = settings.PHOTOS_PER_PAGE
        offset = (page - 1) * limit
        owner = User.get(owner)
        photos = Photo.find_by_owner(owner.id, limit=limit, offset=offset)
        return render(request, 'gallery.html', {
            'owner': owner,
            'photos': photos,
            'current_page': page,
            'page_range': xrange(1, max(2, (owner.ready_photo_count + limit - 1) // limit + 1))
        })
    except User.DoesNotExist:
        return HttpResponseRedirect('/')


def photo(request, owner, nb):
    try:
        photo = Photo.get(owner, nb)
        owner = User.get(owner)
        return render(request, 'photo.html', {
            'owner': owner,
            'photo': photo
        })
    except (Photo.DoesNotExist, User.DoesNotExist):
        return HttpResponseRedirect('/')


def make_reader(f):
    s = f.read()
    while s:
        yield s
        s = f.read()


# tylko tymczasowo...
def photo_file(request, owner, nb):
    storage = Client(domain = settings.MOGILEFS_DOMAIN,
            trackers = settings.MOGILEFS_TRACKERS)
    f = storage.read_file(path.join(settings.UNPROCESSED_PHOTOS_DIR, '%s,%s.jpg' % (owner, nb)))
    return HttpResponse(make_reader(f), content_type='image/jpeg')
    
def photo_thumbnail(request, owner, nb):
    storage = Client(domain = settings.MOGILEFS_DOMAIN,
            trackers = settings.MOGILEFS_TRACKERS)
    f = storage.read_file(path.join(settings.PROCESSED_PHOTOS_DIR, '%s,%s-160x160.jpg' % (owner, nb)))
    return HttpResponse(make_reader(f), content_type='image/jpeg')


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
