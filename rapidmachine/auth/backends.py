# -*- coding: utf-8 -*-
from passlib.hash import bcrypt


class AuthBackend(object):
    """
    Basic auth backend.

    Use one of its subclasses or make your own.
    """
    
    hasher = bcrypt

    def get_user(self, username, password):
        """
        Returns the user with specified username and password
        if it exists and the password is verified; otherwise,
        returns False.
        """
        record = self.read_user(username)
        if not record:
            return False
        if not self.hasher.verify(password, record[self.password_field]):
            return False
        del record[self.password_field]
        return record

    def create_user(self, username, password, data={}):
        """
        Creates a user with specified data.
        """
        raise NotImplemented()

    def read_user(self, username):
        """
        Returns the user with specified username.
        """
        raise NotImplemented()

    def update_user(self, user, data):
        """
        Updates the user with new data.
        """
        raise NotImplemented()

    def delete_user(self, user):
        """
        Deletes the user.
        """
        raise NotImplemented()


class PersistenceAuthBackend(AuthBackend):
    """
    Auth backend that gets data from a subclass of
    :class:`rapidmachine.persistence.Persistence`.
    """

    def __init__(self, persistence,
                username_field="username", password_field="password"):
        self.persistence = persistence
        self.username_field = username_field
        self.password_field = password_field

    def _q(self, username):
        return {self.username_field: username}

    def _qq(self, user):
        return self._q(user[self.username_field])

    def create_user(self, username, password, data={}):
        if self.read_user(username):
            return False
        d = data.copy()
        d[self.username_field] = username
        d[self.password_field] = self.hasher.encrypt(password)
        return self.persistence.create(d)

    def read_user(self, username):
        return self.persistence.read_one(self._q(username))

    def update_user(self, user, data):
        d = user.copy()
        d.update(data)
        if self.password_field in data:
            d[self.password_field] = self.hasher.encrypt(d[self.password_field])
        return self.persistence.update(self._qq(user), d)

    def delete_user(self, user):
        return self.persistence.delete(self._qq(user))
