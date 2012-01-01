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

    def __init__(self, id, desc, status):
        self.id = id
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
                ['id', 'desc', 'status'], str(id)))

        return Photo(int(dat['id']), dat['desc'], dat['status'])

    @staticmethod
    def create(desc):
        hs = Manager()

        # Trochę kiepskie, ale na początek może starczy
        for i in range(NUM_TRIES):
            try:
                newId = str(randint(1, MAX_INT))
                hs.insert(settings.HS_DBNAME, 'photos',
                    [('id', newId), ('desc', desc), ('status', u'n')])
                break
            except OperationalError, e:
                print e
                continue
        else:
            raise Exception("Failed to create Photo!")

        return Photo(newId, desc, u'n')

    # Wyłącznie do testowania, potem usunąć
    @staticmethod
    def all():
        hs = Manager()

        dat = hs.find(settings.HS_DBNAME, 'photos',
                '>=', ['id', 'desc', 'status'], ['1'], None, MAX_INT)

        ret = []

        for r in dat:
            ret.append(Photo(**dict(r)))

        return ret

