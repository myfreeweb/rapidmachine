import t
from should_dsl import *
from passlib.hash import bcrypt
from rapidmachine.persistence import MemoryPersistence
from rapidmachine.auth.backends import PersistenceAuthBackend

# default fields: "username", "password"


class BackendsTest(t.Test):

    def setUp(self):
        self.mp = MemoryPersistence(db=[])
        self.mp.create({
            "username": "user",
            "password": bcrypt.encrypt("pass", rounds=4)
        })
        self.pb = PersistenceAuthBackend(self.mp)

    def test_persistencebackend_valid(self):
        self.pb.get_user("user", "pass")["username"] |should_be.equal_to| "user"

    def test_persistencebackend_invalid_user(self):
        self.pb.get_user("notuser", "wrong") |should_be.equal_to| False

    def test_persistencebackend_invalid_password(self):
        self.pb.get_user("user", "wrong") |should_be.equal_to| False
