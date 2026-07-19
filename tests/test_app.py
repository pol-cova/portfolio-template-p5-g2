import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        TimelinePost.delete().execute()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>" in html and "</title>" in html
        title = html.split("<title>", 1)[1].split("</title>", 1)[0].strip()
        assert title != ""

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_create_and_read(self):
        post_response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": "hello guys"})
        assert post_response.status_code == 200

        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        posts = get_response.get_json()["timeline_posts"]
        assert len(posts) == 1
        assert posts[0]["name"] == "John Doe"
        assert posts[0]["email"] == "john@example.com"
        assert posts[0]["content"] == "hello guys"

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Testing the timeline validation logic!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Testing the timeline validation logic!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
