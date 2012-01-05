
from os import path
from time import sleep
from celery.decorators import task
from PIL import Image

from django.conf import settings

from models import Photo

@task()
def prepare_photo_files(id):
    im = Image.open(path.join(settings.UNPROCESSED_PHOTOS_DIR, '%s.jpg' % id))
    im.thumbnail((160, 160), Image.ANTIALIAS)
    im.save(path.join(settings.PROCESSED_PHOTOS_DIR, "%s-160x160.jpg" % id), "JPEG")

    #sleep(20)
    photo = Photo.get(id)
    photo.update_status(u'r')
