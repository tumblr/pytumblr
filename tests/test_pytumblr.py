# -*- coding: utf-8 -*-

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
        with open('tests/tumblr_credentials.json', 'r') as f:
            credentials = json.loads(f.read())
        self.client = pytumblr.TumblrRestClient(credentials['consumer_key'], credentials['consumer_secret'], credentials['oauth_token'], credentials['oauth_token_secret'])

    @httprettified
    def test_dashboard(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/user/dashboard',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.dashboard()
        assert response['posts'] == []

    @httprettified
    def test_posts(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.posts('codingjester.tumblr.com')
        assert response['posts'] == []

    @httprettified
    def test_posts_with_type(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/seejohnrun.tumblr.com/posts/photo',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.posts('seejohnrun', 'photo')
        assert response['posts'] == []

    @httprettified
    def test_posts_with_type_and_arg(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/seejohnrun.tumblr.com/posts/photo?limit=1',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        args = { 'limit': 1 }
        response = self.client.posts('seejohnrun', 'photo', **args)
        assert response['posts'] == []

    @httprettified
    def test_posts_with_unicode_arg(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/seejohnrun.tumblr.com/posts?tag=voil%C3%A0',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')
        args = { 'tag': u'voilà' }
        response = self.client.posts('seejohnrun', **args)
        assert response['posts'] == []

    @httprettified
    def test_blogInfo(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/info',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"blog": {} } }')

        response = self.client.blog_info('codingjester.tumblr.com')
        assert response['blog'] == {}

    @httprettified
    def test_followers(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/followers',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"users": [] } }')

        response = self.client.followers('codingjester.tumblr.com')
        assert response['users'] == []

    @httprettified
    def test_following(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/following',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"blogs": [], "total_blogs": 1}}')

        response = self.client.following('pytblr.tumblr.com')
        assert response['blogs'] == []

    @httprettified
    def test_blogLikes(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client.blog_likes('codingjester.tumblr.com')
        assert response['liked_posts'] == []

    @httprettified
    def test_blogLikes_with_after(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client.blog_likes('codingjester.tumblr.com', after=1418684291)
        assert response['liked_posts'] == []

    @httprettified
    def test_blogLikes_with_before(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client.blog_likes('codingjester.tumblr.com', before=1418684291)
        assert response['liked_posts'] == []

    @httprettified
    def test_queue(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts/queue',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.queue('codingjester.tumblr.com')
        assert response['posts'] == []

    @httprettified
    def test_drafts(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts/draft',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.drafts('codingjester.tumblr.com')
        assert response['posts'] == []

    @httprettified
    def test_submissions(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/posts/submission',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.submission('codingjester.tumblr.com')
        assert response['posts'] == []

    @httprettified
    def test_follow(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/user/follow',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.follow("codingjester.tumblr.com")
        assert response == []

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['url'][0] == 'codingjester.tumblr.com'

    @httprettified
    def test_unfollow(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/user/unfollow',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.unfollow("codingjester.tumblr.com")
        assert response == []

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['url'][0] == 'codingjester.tumblr.com'

    @httprettified
    def test_reblog(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/seejohnrun.tumblr.com/post/reblog',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.reblog('seejohnrun', id='123', reblog_key="adsfsadf", state='coolguy', tags=['hello', 'world', u'voilà'])
        assert response == []

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == 'POST'
        assert experimental_body['id'][0] == '123'
        assert experimental_body['reblog_key'][0] == 'adsfsadf'
        assert experimental_body['state'][0] == 'coolguy'
        assert experimental_body['tags'][0] == u'hello,world,voilà'.encode('utf-8')

    @httprettified
    def test_edit_post(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/seejohnrun.tumblr.com/post/edit',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.edit_post('seejohnrun', id='123', state='coolguy', tags=['hello', 'world', u'voilà'])
        assert response == []

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == 'POST'
        assert experimental_body['id'][0] == '123'
        assert experimental_body['state'][0] == 'coolguy'
        assert experimental_body['tags'][0] == u'hello,world,voilà'.encode('utf-8')

    @httprettified
    def test_like(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/user/like',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.like('123', "adsfsadf")
        assert response == []

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['id'][0] == '123'
        assert experimental_body['reblog_key'][0] == 'adsfsadf'

    @httprettified
    def test_unlike(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/user/unlike',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.unlike('123', "adsfsadf")
        assert response == []

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['id'][0] == '123'
        assert experimental_body['reblog_key'][0] == 'adsfsadf'

    @httprettified
    def test_info(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/user/info',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.info()
        assert response == []

    @httprettified
    def test_likes(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/user/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.likes()
        assert response == []

    @httprettified
    def test_likes_with_after(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/user/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.likes(after=1418684291)
        assert response == []

    @httprettified
    def test_likes_with_before(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/user/likes',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.likes(before=1418684291)
        assert response == []

    @httprettified
    def test_following(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/user/following',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.following()
        assert response == []

    @httprettified
    def test_tagged(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/tagged?tag=food',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.tagged('food')
        assert response == []

    @httprettified
    def test_tagged_unicode(self):
        HTTPretty.register_uri(HTTPretty.GET, 'https://api.tumblr.com/v2/tagged?tag=voil%C3%A0',
                               body='{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.tagged(u'voilà')
        assert response == []

    @httprettified
    def test_create_text(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_text('codingjester.tumblr.com', body=u"Testing äöü")
        assert response == []

    @httprettified
    def test_create_link(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_link('codingjester.tumblr.com', url="https://google.com", tags=['omg', 'nice', u'voilà'])
        assert response == []

        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert HTTPretty.last_request.method == "POST"
        assert experimental_body['tags'][0] == u"omg,nice,voilà".encode('utf-8')

    @httprettified
    def test_no_tags(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/seejohnrun.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_link('seejohnrun.tumblr.com', tags=[])
        experimental_body = parse_qs(HTTPretty.last_request.body)
        assert 'tags' not in experimental_body

    @httprettified
    def test_create_quote(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_quote('codingjester.tumblr.com', quote=u"It's better to love and lost, than never have loved at all. ♥")
        assert response == []

    @httprettified
    def test_create_chat(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_chat('codingjester.tumblr.com', conversation=u"JB: Testing is rad.\nJC: Hell yeah. ♥")
        assert response == []

    @httprettified
    def test_create_photo_from_url(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_photo('codingjester.tumblr.com', source="https://media.tumblr.com/image.jpg")
        assert response == []


    # For some reason, mocking open causes mimetypes.guess_type to
    # hang. Mocking guess_type isn't ideal since we're overriding part
    # of what we're testing. Find better solution?
    @httprettified
    @mock.patch('mimetypes.guess_type')
    def test_create_photo_from_file(self, mockguess):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')
        mockopen = mock.mock_open(read_data='some data')
        mockguess.return_value = 'jpg'
        with mock.patch('__builtin__.open', mockopen, create=True):
            response = self.client.create_photo('codingjester.tumblr.com', data="/Users/johnb/Desktop/gozer_avatar.jpg")
        assert response == []

    @httprettified
    @mock.patch('mimetypes.guess_type')
    def test_create_photo_from_file_with_unicode(self, mockguess):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')
        mockopen = mock.mock_open(read_data='some data')
        mockguess.return_value = 'jpg'
        with mock.patch('__builtin__.open'.format(__name__), mockopen, create=True):
           response = self.client.create_photo('codingjester.tumblr.com', data=u"/Users/johnb/Desktop/gözer_avatar.jpg")
        assert response == []

    @httprettified
    def test_create_audio(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_audio('codingjester.tumblr.com', external_url="https://media.tumblr.com/audio.mp3")
        assert response == []

    @httprettified
    def test_create_video(self):
        HTTPretty.register_uri(HTTPretty.POST, 'https://api.tumblr.com/v2/blog/codingjester.tumblr.com/post',
                               body='{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_video('codingjester.tumblr.com', embed="blahblahembed")
        assert response == []

if __name__ == "__main__":
    unittest.main()
