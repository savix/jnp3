# -*- coding: utf-8 -*-

from random import randint

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from pyhs import Manager

import jnp3.hsdb as hsdb

from sphinxsearch import SphinxClient


class Photo:
    def __init__(self, owner, nb, status, desc):
        self.owner = int(owner)
        self.nb = abs(int(nb))
        self.desc = desc
        self.status = status
    
    def ready(self):
        hsdb.update('photos', ('owner', 'nb', 'status'), '=', (self.owner, -self.nb), (self.owner, -self.nb, 'r'))
        # To powinno działać - jak nie to się przepisze
        hsdb.incr('users', ('ready_photos', ), '=', (self.owner, ))
        self.status = 'r'

    @staticmethod
    def get(owner, nb):
        rows = hsdb.find('photos', ('owner', 'nb', 'status', 'desc'), '=', (owner, -abs(int(nb))), limit=1)
        if rows:
            row = rows[0]
            return Photo(row['owner'], row['nb'], row['status'], row['desc'])
        else:
            raise Photo.DoesNotExist()

    @staticmethod
    def find_by_owner(owner, limit, offset):
        rows = hsdb.find('photos', ('owner', 'status', 'nb', 'desc'), '=', (owner, 'r'),
            index_name='photos_by_owner_status_nb', limit=limit, offset=offset)
        return [Photo(**row) for row in rows]

    @staticmethod
    def find_by_desc(query, limit, offset, owners=None):
        # szuka w desc używając sphinxa
        # można dać zbiór owner ids i wtedy zwróci wynik tylko dla nich
        sc = SphinxClient()
        sc.SetServer('localhost', settings.SPHINX_PORT)
        sc.SetLimits(offset, limit)

        if owners != None:
            sc.SetFilter('owner', owners)

        ans = sc.Query(query, settings.SPHINX_INDEX)
        ret = []

        for r in ans['matches']:
            try:
                # brzydki hack pod sphinxa
                nb = int(r['attrs']['nb'])

                if nb > 2**31:
                    nb = 2**32 - nb

                ret.append(Photo.get(r['attrs']['owner'], nb))
            except Photo.DoesNotExist:
                print "hoho", nb
                # Nie martwimy się tym
                pass

        # liczba wszystkich zmatchowanych
        totalFound = ans['total_found']

        return (ret, totalFound)

    @staticmethod
    def create(owner, desc):
        nb = hsdb.incr('users', ('all_photos', ), '=', (owner, ), return_original=True)[0]['all_photos']
        hsdb.insert('photos', ('owner', 'nb', 'status', 'desc'), (owner, -int(nb), 'n', desc))
        return Photo(owner, nb, 'n', desc)

    class DoesNotExist(ObjectDoesNotExist):
        pass
