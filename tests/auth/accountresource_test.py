import t
from should_dsl import *
from base64 import b64encode
from rapidmachine import App, Route
from rapidmachine.persistence import MemoryPersistence
from rapidmachine.auth import AccountResource, PersistenceAuthBackend


mp = MemoryPersistence()
pab = PersistenceAuthBackend(mp)


class TestAccountResource(AccountResource):

    backend = pab


class AccountTestApp(App):

    handlers = [
        Route("account").to(TestAccountResource)
    ]
    auth_backend = pab


class AccountTest(t.Test):

    def setUp(self):
        self.client = AccountTestApp().test_client()

    def test_create(self):
        rsp = self.client.post("/account", content_type="application/json",
                data='{"username":"writer","password":"hello"}')
        mp.read_one({"username": "writer"})["password"] |should_not_be.equal_to| "hello"
        rsp.status_code |should_be.equal_to| 303
        rsp.headers["location"] |should_be.equal_to| "http://localhost/account"

        rsp = self.client.post("/account", content_type="application/json",
                data='{"username":"writer","password":"hello"}')
        rsp.status_code |should_be.equal_to| 400

        rsp = self.client.post("/account", content_type="application/json",
                data='{"username":"testname"}')
        rsp.status_code |should_be.equal_to| 400

        rsp = self.client.post("/account", content_type="application/json",
                data='{"password":"testname"}')
        rsp.status_code |should_be.equal_to| 400

    def test_read(self):
        pab.create_user("reader", "hello")
        rsp = self.client.get("/account", headers={
            "Accept": "application/json",
            "Authorization": "Basic "+b64encode("reader:hello")
        })
        rsp.status_code |should_be.equal_to| 200
        rsp.data |should_be.equal_to| '{"username": "reader"}'

    def test_update(self):
        pab.create_user("updater", "hello")
        rsp = self.client.put("/account", content_type="application/json",
                headers={"Authorization": "Basic "+b64encode("updater:hello")},
                data='{"city":"Moscow"}')
        u = mp.read_one({"username": "updater"})
        u["city"] |should_be.equal_to| "Moscow"
        oldhash = u["password"]

        rsp = self.client.put("/account", content_type="application/json",
                headers={"Authorization": "Basic "+b64encode("updater:hello")},
                data='{"password":"second"}')
        u = mp.read_one({"username": "updater"})
        u["password"] |should_not_be.equal_to| oldhash
        u["password"] |should_not_be.equal_to| "second"

    def test_delete(self):
        pab.create_user("deleter", "hello")
        rsp = self.client.delete("/account",
                headers={"Authorization": "Basic "+b64encode("deleter:hello")})
        mp.read_one({"username": "deleter"}) |should_be.equal_to| None
