from celery.decorators import task
from time import sleep

from models import Photo

@task()
def prepare_photo_files(id):
    sleep(20)
    photo = Photo.get(id)
    photo.update_status(u'r')
