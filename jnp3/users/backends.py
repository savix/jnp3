# -*- coding: utf-8 -*-

from models import User

class AuthBackend(object):
    
    def authenticate(self, username, password):
        try:
            user = User.get_by_username(username)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        return User.get(user_id)
