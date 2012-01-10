# -*- coding: utf-8 -*-

from django.contrib.auth.models import check_password, get_hexdigest
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

users = (
    (1, 'user1', 'user1'),
    (2, 'user2', 'user2'),
)

def hash_password(raw_password):
    import random
    algo = 'sha1'
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, raw_password)
    return '%s$%s$%s' % (algo, salt, hsh)

class User(object):
    
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
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
        for current_id, current_username, current_raw_password in users:
            if current_id == id:
                return User(current_id, current_username, hash_password(current_raw_password))
        raise User.DoesNotExist()
    
    @staticmethod
    def create(username, password):
        raise NotImplementedError()
    
    @staticmethod
    def get_by_username(username):
        for current_id, current_username, current_raw_password in users:
            if current_username == username:
                return User(current_id, current_username, hash_password(current_raw_password))
        raise User.DoesNotExist()
    
    class DoesNotExist(ObjectDoesNotExist):
        pass
