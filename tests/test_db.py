import unittest
from datetime import datetime

from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='hello guys', created_at=datetime(2020, 1, 1))
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jame@example.com', content='hello friends', created_at=datetime(2020, 1, 2))
        assert second_post.id == 2

        posts = list(TimelinePost.select().order_by(TimelinePost.created_at.desc()))
        assert len(posts) == 2
        assert posts[0].content == 'hello friends'
        assert posts[1].content == 'hello guys'
