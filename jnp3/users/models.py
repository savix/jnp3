# -*- coding: utf-8 -*-

from django.contrib.auth.models import check_password, get_hexdigest
from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

import jnp3.hsdb as hsdb

def hash_password(raw_password):
    import random
    algo = 'sha1'
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, raw_password)
    return '%s$%s$%s' % (algo, salt, hsh)

class User(object):
    
    def __init__(self, id, username, password, ready_photo_count):
        self.id = int(id)
        self.username = username
        self.password = password
        self.ready_photo_count = int(ready_photo_count)
    
    @property
    def is_staff(self):
        return False
    
    @property
    def is_active(self):
        return True
        
    @property
    def is_superuser(self):
        return False
    
    @property
    def groups(self):
        return ()
    
    @property
    def user_permissions(self):
        return ()
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True
    
    def set_password(self, raw_password):
        # Tak może zostać
        raise NotImplementedError()
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def save(self):
        # AuthenticationForm ustawia czas ostatniego logowania
        # my to olewamy, ale niech myśli, że się zapisało
        pass
    
    def delete(self):
        # Tak może zostać
        raise NotImplementedError()
    
    def __unicode__(self):
        return self.username
    
    @staticmethod
    def get(id):
        row = hsdb.get('users', ('id', 'username', 'password', 'ready_photos'), id)
        if row:
            return User(row['id'], row['username'], row['password'], row['ready_photos'])
        else:
            raise User.DoesNotExist()
    
    @staticmethod
    def create(username, password):
        password = hash_password(password)
        try:
            hsdb.insert('users', ('id', 'username', 'password', 'ready_photos', 'all_photos'),
                ('', username, password, 0, 0))
        except hsdb.OperationalError:
            raise IntegrityError()
        else:
            row = hsdb.get('users', ('username', 'id'), username, index_name='users_by_username')
            return User(row['id'], username, password, 0)
    
    @staticmethod
    def get_by_username(username):
        row = hsdb.get('users', ('username', 'id', 'password', 'ready_photos'), username,
            index_name='users_by_username')
        if row:
            return User(row['id'], row['username'], row['password'], row['ready_photos'])
        else:
            raise User.DoesNotExist()
    
    class DoesNotExist(ObjectDoesNotExist):
        pass
