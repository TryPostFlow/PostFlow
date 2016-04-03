
from ._base import BaseCase


class TestAccount(BaseCase):
    def test_new_account(self):
        data = dict(
            name='test_name_1',
            email='test_email_1@test.com',
            password='test_password_1')

        response = self.post("/accounts", data=data)
        print response
        assert response["name"] == data["name"]

    def test_get_account(self):
        data = dict(
            name='test_name_1',
            email='test_email_1@test.com',
            password='test_password_1')

        response_1 = self.post("/accounts", data=data)

        response = self.get("/accounts/%d" % response_1['id'])
        assert response["name"] == data['name']

    def test_list_posts(self):
        data = dict(
            name='test_name_1',
            email='test_email_1@test.com',
            password='test_password_1')

        self.post("/accounts", data=data)

        data = dict(
            name='test_name_2',
            email='test_email_2@test.com',
            password='test_password_2')

        self.post("/accounts", data=data)

        response = self.get("/accounts")
        assert len(response) == 2
