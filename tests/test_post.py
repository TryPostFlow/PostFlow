
from ._base import BaseCase


class TestPost(BaseCase):
    def test_new_post(self):
        data = dict(
            title='test1',
            slug='test1',
            content='test content')

        response = self.post("/posts", data=data)
        assert response["title"] == "test1"

    def test_get_post(self):
        data = dict(
            title='test1',
            slug='test1',
            content='test content')

        self.post("/posts", data=data)

        response = self.get("/posts/1")
        assert response["title"] == "test1"

    def test_list_posts(self):
        data = dict(
            title='test1',
            slug='test1',
            content='test content')

        self.post("/posts", data=data)

        data = dict(
            title='test2',
            slug='test2',
            content='test content2')

        self.post("/posts", data=data)

        response = self.get("/posts")
        print response
        assert len(response) == 2
