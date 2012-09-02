# -*- coding: utf-8 -*-
from passlib.hash import bcrypt


class AuthBackend(object):
    """
    Basic auth backend.

    All methods here (except __init__ and verify) just raise NotImplemented.
    Use one of its subclasses or make your own.
    """

    def encrypt(self, password):
        """
        Hashes the password.
        Uses bcrypt; to use a different hash, override this method.
        """
        return bcrypt.encrypt(password)

    def verify(self, password, entered_password):
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

    def get_user(self, username, password):
        record = self.persistence.read_one({self.username_field: username})
        if not record:
            return False
        if not self.verify(record[self.password_field], password):
            return False
        return record
