import os
import json
import unittest
from server import app


class BaseCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK'] = 'test'
        self.app = app
        with self.app.app_context():
            self.app.db.create_all()

        self.client = self.app.test_client()

    def post(self, url, data):
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json')
        return json.loads(response.get_data(as_text=True))

    def get(self, url):
        response = self.client.get(
            url,
            content_type='application/json')
        return json.loads(response.get_data(as_text=True))

    def put(self, url, data):
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json')
        return json.loads(response.get_data(as_text=True))


    def tearDown(self):
        with self.app.app_context():
            self.app.db.drop_all()
