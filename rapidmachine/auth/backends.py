# -*- coding: utf-8 -*-
from passlib.hash import bcrypt


class AuthBackend(object):

    def get_user(self, username, password):
        raise NotImplemented


class PersistenceAuthBackend(AuthBackend):

    def __init__(self, persistence,
                username_field="username", password_field="password"):
        self.persistence = persistence
        self.username_field = username_field
        self.password_field = password_field

    def verify(self, password, entered_password):
        return bcrypt.verify(entered_password, password)

    def get_user(self, username, password):
        record = self.persistence.read_one({self.username_field: username})
        if not record:
            return False
        if not self.verify(record[self.password_field], password):
            return False
        return record
