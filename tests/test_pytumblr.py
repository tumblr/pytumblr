import nose
import unittest
import mock
import json
import io
from httpretty import HTTPretty, httprettified
import pytumblr
from urlparse import parse_qs


class TumblrRestClientTest(unittest.TestCase):
    """
    """

    def setUp(self):
        credentials = json.loads(open('tests/tumblr_credentials.json', 'r').read())
        self.client = pytumblr.TumblrRestClient(credentials['consumer_key'], credentials['consumer_secret'], credentials['oauth_token'], credentials['oauth_token_secret'])

    @httprettified
    def test_dashboard(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/user/dashboard',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.dashboard()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
        assert response['response']['posts'] == []

    @httprettified
    def test_posts(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.posts('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
        assert response['response']['posts'] == []

    @httprettified
    def test_blogInfo(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/info',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"blog": {} } }')

        response = self.client.blog_info('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
        assert response['response']['blog'] == {}

    @httprettified
    def test_followers(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/followers',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"users": [] } }')

        response = self.client.followers('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
        assert response['response']['users'] == []

    @httprettified
    def test_blogLikes(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client.blog_likes('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_queue(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts/queue',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.queue('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_drafts(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts/draft',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.drafts('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_submissions(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts/submission',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.submission('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_follow(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/user/follow',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.follow("codingjester.tumblr.com")
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['url'][0] == 'codingjester.tumblr.com'

    @httprettified
    def test_unfollow(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/user/unfollow',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.unfollow("codingjester.tumblr.com")
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['url'][0] == 'codingjester.tumblr.com'

    @httprettified
    def test_like(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/user/like',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.like('123', "adsfsadf")
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['id'][0] == '123'
        assert experimental_body['reblog_key'][0] == 'adsfsadf'

    @httprettified
    def test_unlike(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/user/unlike',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.unlike('123', "adsfsadf")
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['id'][0] == '123'
        assert experimental_body['reblog_key'][0] == 'adsfsadf'

    @httprettified
    def test_info(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/user/info',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.info()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_likes(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/user/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.likes()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_following(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/user/following',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.following()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_tagged(self):
        HTTPretty.register_uri(HTTPretty.GET, 'http://api.tumblr.com/v2/tagged?tag=food',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.tagged('food')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_create_text(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_text('codingjester.tumblr.com', body="Testing")
        assert response['meta']['status'] == 201
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_create_link(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_link('codingjester.tumblr.com', url="http://google.com", tags=['omg', 'nice'])
        assert response['meta']['status'] == 201
        assert response['meta']['msg'] == "OK"

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['tags'][0] == "omg,nice"

    @httprettified
    def test_create_text(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_quote('codingjester.tumblr.com', quote="It's better to love and lost, than never have loved at all.")
        assert response['meta']['status'] == 201
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_create_text(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_chat('codingjester.tumblr.com', conversation="JB: Testing is rad.\nJC: Hell yeah.")
        assert response['meta']['status'] == 201
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_create_photo(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_photo('codingjester.tumblr.com', source="http://media.tumblr.com/image.jpg")
        assert response['meta']['status'] == 201
        assert response['meta']['msg'] == "OK"

        #with mock.patch('__builtin__.open') as my_mock:
        #    my_mock.return_value.__enter__ = lambda s: s
        #    my_mock.return_value.__exit__ = mock.Mock()
        #    my_mock.return_value.read.return_value = 'some data'
        #    response = self.client.create_photo('codingjester.tumblr.com', data="/Users/johnb/Desktop/gozer_avatar.jpgdf")
        #    assert response['meta']['status'] == 201
        #    assert response['meta']['msg'] == "OK"

        #response = self.client.create_photo('codingjester.tumblr.com', data=["/Users/johnb/Desktop/gozer_avatar.jpg", "/Users/johnb/Desktop/gozer_avatar.jpg"])
        #assert response['meta']['status'] == 201
        #assert response['meta']['msg'] == "OK"

    @httprettified
    def test_create_audio(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_audio('codingjester.tumblr.com', external_url="http://media.tumblr.com/audio.mp3")
        assert response['meta']['status'] == 201
        assert response['meta']['msg'] == "OK"

    @httprettified
    def test_create_video(self):
        HTTPretty.register_uri(HTTPretty.POST, 'http://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_video('codingjester.tumblr.com', embed="blahblahembed")
        assert response['meta']['status'] == 201
        assert response['meta']['msg'] == "OK"

if __name__ == "__main__":
    unittest.main()
