# -*- coding: utf-8 -*-

from random import randint

from django.conf import settings
from pyhs import Manager
from pyhs.exceptions import OperationalError

MAX_INT = 2147483647
NUM_TRIES = 20

class Photo:
#    STATUS_CHOICES = (
#        (u'n', u'new'),
#        (u'r', u'ready'),
#        (u'd', u'deleted'),
#    )

    def __init__(self, id, owner, desc, status):
        self.id = id
        self.owner = owner
        self.desc = desc
        self.status = status

    def update_status(self, status):
        hs = Manager()

        hs.update(settings.HS_DBNAME, 'photos',
                '=', ['id', 'status'], [str(self.id)],
                [str(self.id), status])

        self.status = status

    @staticmethod
    def get(id):
        hs = Manager()

        dat = dict(hs.get(settings.HS_DBNAME, 'photos',
                ['id', 'owner', 'desc', 'status'], str(id)))

        return Photo(int(dat['id']), int(dat['owner']), dat['desc'], dat['status'])

    @staticmethod
    def find_by_owner(owner, start, end, status='r'):
        # TODO to trzeba poprawić, może trzeba założyć indeks?
        # No i skąd wziąć łączną liczbę zdjęć?
        return Photo.all()
    
    @staticmethod
    def create(owner, desc):
        hs = Manager()

        # Trochę kiepskie, ale na początek może starczy
        for i in range(NUM_TRIES):
            try:
                newId = str(randint(1, MAX_INT))
                hs.insert(settings.HS_DBNAME, 'photos',
                    [('id', newId), ('owner', str(owner)), ('desc', desc), ('status', u'n')])
                break
            except OperationalError, e:
                print e
                continue
        else:
            raise Exception("Failed to create Photo!")

        return Photo(newId, owner, desc, u'n')

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

