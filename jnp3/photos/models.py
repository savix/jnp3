# -*- coding: utf-8 -*-

from random import randint

from django.conf import settings
from pyhs import Manager
from pyhs.exceptions import OperationalError

MAX_INT = 2147483647
NUM_TRIES = 20

class Photo:
#    STATUS_CHOICES = (
#        ('n', 'new'),
#        ('r', 'ready'),
#    )

    def __init__(self, id, owner, desc, status):
        self.id = id
        self.owner = owner
        self.desc = desc
        self.status = status

    def ready(self):
        hs = Manager()

        hs.update(settings.HS_DBNAME, 'photos',
                '=', ['id', 'status'], [str(self.id)],
                [str(self.id), 'r'])

        # zakładam, że nie mamy usuwania zdjęć
        hs.incr(settings.HS_DBNAME, 'owners',
                '=', ['owner', 'num_photos'], [str(self.owner)], ['0', '1'])

        self.status = 'r'

    @staticmethod
    def get(id):
        hs = Manager()

        dat = dict(hs.get(settings.HS_DBNAME, 'photos',
                ['id', 'owner', 'desc', 'status'], str(id)))

        return Photo(int(dat['id']), int(dat['owner']), dat['desc'],
                dat['status'])

    @staticmethod
    def find_by_owner(owner, limit, offset):
        # zamieniłem na limit i offset, żeby uniknąć problemów
        # szuka tylko w gotowych zdjęciach
        hs = Manager()

        dat = hs.find(settings.HS_DBNAME, 'photos',
                '=', ['owner', 'status', 'id', 'desc'],
                [str(owner), 'r'],
                'owner_status_id', str(limit), str(offset))

        ret = []

        for r in dat:
            ret.append(Photo(**dict(r)))

        return ret

    @staticmethod
    def get_num_photos(owner):
        # zwraca liczbę zdjęć ownera ze statusem 'r'
        hs = Manager()

        dat = dict(hs.get(settings.HS_DBNAME, 'owners',
                ['owner', 'num_photos'], str(owner)))

        return dat['num_photos']

    @staticmethod
    def create(owner, desc):
        hs = Manager()

        # Trochę kiepskie, ale na początek może starczy
        for i in range(NUM_TRIES):
            try:
                newId = str(randint(1, MAX_INT))
                hs.insert(settings.HS_DBNAME, 'photos',
                    [('id', newId), ('owner', str(owner)), ('desc', desc),
                        ('status', 'n')])
                break
            except OperationalError, e:
                print e
                continue
        else:
            raise Exception("Failed to create Photo!")

        return Photo(newId, owner, desc, 'n')

    # Wyłącznie do testowania, potem usunąć
    @staticmethod
    def all():
        hs = Manager()

        dat = hs.find(settings.HS_DBNAME, 'photos',
                '>=', ['id', 'owner', 'desc', 'status'], ['1'], None, MAX_INT)

        ret = []

        for r in dat:
            ret.append(Photo(**dict(r)))

        return ret

