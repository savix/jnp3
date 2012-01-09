
from os import path
from time import sleep
from celery.decorators import task
from PIL import Image

from django.conf import settings

from models import Photo

from pymogile import Client, MogileFSError

@task()
def prepare_photo_files(id):
    storage = Client(domain = settings.MOGILEFS_DOMAIN,
            trackers = settings.MOGILEFS_TRACKERS)
    #im = Image.open(path.join(settings.UNPROCESSED_PHOTOS_DIR, '%s.jpg' % id))
    f = storage.read_file(path.join(settings.UNPROCESSED_PHOTOS_DIR, '%s.jpg' % id))
    im = Image.open(f)
    im.thumbnail((160, 160), Image.ANTIALIAS)

    tn = storage.new_file(path.join(settings.PROCESSED_PHOTOS_DIR, '%s-160x160.jpg' % id))
    im.save(tn, 'JPEG')

    #sleep(20)
    photo = Photo.get(id)
    photo.ready()
