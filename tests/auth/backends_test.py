import t
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

    def test_persistencebackend_valid(self):
        pb = PersistenceAuthBackend(self.mp)
        t.eq(pb.get_user("user", "pass")["username"], "user")

    def test_persistencebackend_invalid_user(self):
        pb = PersistenceAuthBackend(self.mp)
        t.eq(pb.get_user("notuser", "wrong"), False)

    def test_persistencebackend_invalid_password(self):
        pb = PersistenceAuthBackend(self.mp)
        t.eq(pb.get_user("user", "wrong"), False)
