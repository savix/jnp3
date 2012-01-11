"""
HandlerSocket backend for sessions in django.
Requires pyhs handlersocket bindings.
"""
from datetime import datetime
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.core.exceptions import SuspiciousOperation
from django.utils.encoding import force_unicode

import hsdb


TABLE_NAME = 'sessions'

class SessionStore(SessionBase):

    def load(self):
        row = hsdb.get(TABLE_NAME, ('session_key', 'session_data', 'expire_date'), self.session_key)
        if row and datetime.now() <= datetime.strptime(row['expire_date'], '%Y-%m-%d %H:%M:%S'):
            return self.decode(force_unicode(row['session_data']))
        else:
            self.create()
            return {}

    def exists(self, session_key):
        """
        Check if session exists.
        """
        return bool(hsdb.get(TABLE_NAME, ('session_key', ), session_key))

    def create(self):
        """
        Create session.
        """
        while True:
            self.session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False):
        values = (
            self.session_key,
            self.encode(self._get_session(no_load=must_create)),
            self.get_expiry_date().strftime('%Y-%m-%d %H:%M:%S'),
        )
            
        if self.exists(self.session_key):
            if must_create:
                raise CreateError
                
            hsdb.update(TABLE_NAME, ('session_key', 'session_data', 'expire_date'), '=',
                (self.session_key, ), values)
        else:
            hsdb.insert(TABLE_NAME, ('session_key', 'session_data', 'expire_date'), values)
            
    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key

        hsdb.delete(TABLE_NAME, ('session_key', ), '=', (session_key, ))
