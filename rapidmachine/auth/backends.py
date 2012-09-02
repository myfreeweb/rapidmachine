# -*- coding: utf-8 -*-
from passlib.hash import bcrypt


class AuthBackend(object):
    """
    Basic auth backend.

    Use one of its subclasses or make your own.
    """

    def encrypt(self, password):
        """
        Hashes the password.
        Uses bcrypt; to use a different hash, override this method.
        """
        return bcrypt.encrypt(password)

    def verify(self, entered_password, password):
        """
        Checks if entered_password matches password.
        Uses bcrypt; to use a different hash, override this method.
        """
        return bcrypt.verify(entered_password, password)

    def get_user(self, username, password):
        """
        Returns the user with specified username and password
        if it exists and the password is verified; otherwise,
        returns False.
        """
        record = self.read_user(username)
        if not record:
            return False
        if not self.verify(password, record[self.password_field]):
            return False
        return record

    def read_user(self, username):
        """
        Returns the user with specified username.
        """
        raise NotImplemented()

    def update_user(self, username, new_username=None, new_password=None, fields={}):
        """
        Updates the user with specified username
        with new username, password and fields.
        """
        raise NotImplemented()

    def delete_user(self, username):
        """
        Deletes the user with specified username.
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

    def read_user(self, username):
        return self.persistence.read_one(self._q(username))

    def update_user(self, username, new_username=None, new_password=None, fields={}):
        for f in [self.username_field, self.password_field]:
            if fields[f]:
                del fields[f]
        if new_username:
            fields[self.username_field] = new_username
        if new_password:
            fields[self.password_field] = self.encrypt(new_password)
        return self.persistence.update(self._q(username), fields)

    def delete_user(self, username):
        return self.persistence.delete(self._q(username))
