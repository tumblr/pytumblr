from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
import unittest
import mock
import json
import pytumblr
import urllib.parse
from urllib.parse import parse_qs
import sys
if sys.version_info < (2, 7):
    # python 2.6 may show ssl warnings, which we don't care about for these tests
    import urllib3
    urllib3.disable_warnings()


def wrap_response(response_text):
    def inner(*args, **kwargs):
        mp = mock.MagicMock()
        mp.json.return_value = json.loads(response_text)
        return mp
    return inner


def wrap_response_storing_data(response_text, store):
    def inner(*args, **kwargs):
        # store data for assertion on input
        store.data = kwargs.get('data')

        mp = mock.MagicMock()
        mp.json.return_value = json.loads(response_text)
        return mp
    return inner


class TumblrRestClientTest(unittest.TestCase):
    """
    """

    def setUp(self):
        with open('tests/tumblr_credentials.json', 'r') as f:
            credentials = json.loads(f.read())
        self.client = pytumblr.TumblrRestClient(credentials['consumer_key'], credentials['consumer_secret'], credentials['oauth_token'], credentials['oauth_token_secret'])

    @mock.patch('requests.get')
    def test_dashboard(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.dashboard()
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_posts(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.posts('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_posts_with_type(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.posts('seejohnrun', 'photo')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_posts_with_type_and_arg(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        args = {'limit': 1}
        response = self.client.posts('seejohnrun', 'photo', **args)
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_blogInfo(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"blog": {} } }')

        response = self.client.blog_info('codingjester.tumblr.com')
        assert response['blog'] == {}

    @mock.patch('requests.get')
    def test_avatar_with_301(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 301, "msg": "Moved Permanently"}, "response": {"avatar_url": "" } }')

        response = self.client.avatar('staff.tumblr.com')
        assert response['avatar_url'] == ''

    @mock.patch('requests.get')
    def test_avatar_with_302(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 302, "msg": "Found"}, "response": {"avatar_url": "" } }')

        response = self.client.avatar('staff.tumblr.com')
        assert response['avatar_url'] == ''

    @mock.patch('requests.get')
    def test_followers(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"users": [] } }')

        response = self.client.followers('codingjester.tumblr.com')
        assert response['users'] == []

    @mock.patch('requests.get')
    def test_blog_following(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"blogs": [], "total_blogs": 1}}')

        response = self.client.blog_following('pytblr.tumblr.com')
        assert response['blogs'] == []

    @mock.patch('requests.get')
    def test_blogLikes(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client.blog_likes('codingjester.tumblr.com')
        assert response['liked_posts'] == []

    @mock.patch('requests.get')
    def test_blogLikes_with_after(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client.blog_likes('codingjester.tumblr.com', after=1418684291)
        assert response['liked_posts'] == []

    @mock.patch('requests.get')
    def test_blogLikes_with_before(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client.blog_likes('codingjester.tumblr.com', before=1418684291)
        assert response['liked_posts'] == []

    @mock.patch('requests.get')
    def test_queue(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.queue('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_drafts(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.drafts('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_submissions(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client.submission('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.post')
    def test_follow(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client.follow("codingjester.tumblr.com")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('url=codingjester.tumblr.com')

    @mock.patch('requests.post')
    def test_unfollow(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client.unfollow("codingjester.tumblr.com")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('url=codingjester.tumblr.com')

    @mock.patch('requests.post')
    def test_reblog(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client.reblog('seejohnrun', id='123', reblog_key="adsfsadf", state='coolguy', tags=['hello', 'world'])
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('state=coolguy&reblog_key=adsfsadf&id=123&tags=hello%2Cworld')

    @mock.patch('requests.post')
    def test_edit_post(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client.edit_post('seejohnrun', id='123', state='coolguy', tags=['hello', 'world'])
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('state=coolguy&id=123&tags=hello%2Cworld')

    @mock.patch('requests.post')
    def test_like(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client.like('123', "adsfsadf")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('id=123&reblog_key=adsfsadf')

    @mock.patch('requests.post')
    def test_unlike(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client.unlike('123', "adsfsadf")
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('id=123&reblog_key=adsfsadf')

    @mock.patch('requests.get')
    def test_info(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.info()
        assert response == []

    @mock.patch('requests.get')
    def test_likes(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.likes()
        assert response == []

    @mock.patch('requests.get')
    def test_likes_with_after(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.likes(after=1418684291)
        assert response == []

    @mock.patch('requests.get')
    def test_likes_with_before(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.likes(before=1418684291)
        assert response == []

    @mock.patch('requests.get')
    def test_following(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.following()
        assert response == []

    @mock.patch('requests.get')
    def test_tagged(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client.tagged('food')
        assert response == []

    @mock.patch('requests.post')
    def test_create_text(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_text('codingjester.tumblr.com', body="Testing")
        assert response == []

    @mock.patch('requests.post')
    def test_create_link(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 201, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client.create_link('codingjester.tumblr.com', url="https://google.com", tags=['omg', 'nice'])
        assert response == []

        assert parse_qs(mock_post.data) == parse_qs('url=https%3A%2F%2Fgoogle.com&type=link&tags=omg%2Cnice')

    @mock.patch('requests.post')
    def test_no_tags(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 201, "msg": "OK"}, "response": []}',
            mock_post)

        self.client.create_link('seejohnrun.tumblr.com')
        
        assert parse_qs(mock_post.data) == parse_qs('type=link&tags=')

    @mock.patch('requests.post')
    def test_create_quote(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_quote('codingjester.tumblr.com', quote="It's better to love and lost, than never have loved at all.")
        assert response == []

    @mock.patch('requests.post')
    def test_create_chat(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_chat('codingjester.tumblr.com', conversation="JB: Testing is rad.\nJC: Hell yeah.")
        assert response == []

    @mock.patch('requests.post')
    def test_create_photo(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_photo('codingjester.tumblr.com', source="https://media.tumblr.com/image.jpg")
        assert response == []

    @mock.patch('requests.post')
    def test_create_audio(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_audio('codingjester.tumblr.com', external_url="https://media.tumblr.com/audio.mp3")
        assert response == []

    @mock.patch('requests.post')
    def test_create_video(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client.create_video('codingjester.tumblr.com', embed="blahblahembed")
        assert response == []


class TumblrRestClient2Test(unittest.TestCase):
    """
    """
    def setUp(self):
        with open('tests/tumblr_credentials2.json', 'r') as f:
            credentials = json.loads(f.read(), strict=False)
        # print (credentials['client_id'])
        token = eval(credentials['token'].encode('utf-8'))
        print (token)
        # print (credentials['client_id'])
        # print (credentials['token'])
        self.client2 = pytumblr.TumblrRestClient2(credentials['client_id'], token)

    @mock.patch('requests.get')
    def test_dashboard(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client2.dashboard()
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_posts(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client2.posts('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_posts_with_type(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client2.posts('seejohnrun', 'photo')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_posts_with_type_and_arg(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        args = {'limit': 1}
        response = self.client2.posts('seejohnrun', 'photo', **args)
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_blogInfo(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"blog": {} } }')

        response = self.client2.blog_info('codingjester.tumblr.com')
        assert response['blog'] == {}

    @mock.patch('requests.get')
    def test_avatar_with_301(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 301, "msg": "Moved Permanently"}, "response": {"avatar_url": "" } }')

        response = self.client2.avatar('staff.tumblr.com')
        assert response['avatar_url'] == ''

    @mock.patch('requests.get')
    def test_avatar_with_302(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 302, "msg": "Found"}, "response": {"avatar_url": "" } }')

        response = self.client2.avatar('staff.tumblr.com')
        assert response['avatar_url'] == ''

    @mock.patch('requests.get')
    def test_followers(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"users": [] } }')

        response = self.client2.followers('codingjester.tumblr.com')
        assert response['users'] == []

    @mock.patch('requests.get')
    def test_blog_following(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"blogs": [], "total_blogs": 1}}')

        response = self.client2.blog_following('pytblr.tumblr.com')
        assert response['blogs'] == []

    @mock.patch('requests.get')
    def test_blogLikes(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client2.blog_likes('codingjester.tumblr.com')
        assert response['liked_posts'] == []

    @mock.patch('requests.get')
    def test_blogLikes_with_after(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client2.blog_likes('codingjester.tumblr.com', after=1418684291)
        assert response['liked_posts'] == []

    @mock.patch('requests.get')
    def test_blogLikes_with_before(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"liked_posts": [] } }')

        response = self.client2.blog_likes('codingjester.tumblr.com', before=1418684291)
        assert response['liked_posts'] == []

    @mock.patch('requests.get')
    def test_queue(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client2.queue('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_drafts(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client2.drafts('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.get')
    def test_submissions(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": {"posts": [] } }')

        response = self.client2.submission('codingjester.tumblr.com')
        assert response['posts'] == []

    @mock.patch('requests.post')
    def test_follow(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client2.follow("codingjester.tumblr.com")
        assert response == []

        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('url=codingjester.tumblr.com')

    @mock.patch('requests.post')
    def test_unfollow(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client2.unfollow("codingjester.tumblr.com")
        assert response == []

        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('url=codingjester.tumblr.com')

    @mock.patch('requests.post')
    def test_reblog(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client2.reblog('seejohnrun', id='123', reblog_key="adsfsadf", state='coolguy', tags=['hello', 'world'])
        assert response == []

        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('state=coolguy&reblog_key=adsfsadf&id=123&tags=hello%2Cworld')

    @mock.patch('requests.post')
    def test_edit_post(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client2.edit_post('seejohnrun', id='123', state='coolguy', tags=['hello', 'world'])
        assert response == []

        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('state=coolguy&id=123&tags=hello%2Cworld')

    @mock.patch('requests.post')
    def test_like(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client2.like('123', "adsfsadf")
        assert response == []

        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('id=123&reblog_key=adsfsadf')

    @mock.patch('requests.post')
    def test_unlike(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 200, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client2.unlike('123', "adsfsadf")
        assert response == []

        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('id=123&reblog_key=adsfsadf')

    @mock.patch('requests.get')
    def test_info(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client2.info()
        assert response == []

    @mock.patch('requests.get')
    def test_likes(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client2.likes()
        assert response == []

    @mock.patch('requests.get')
    def test_likes_with_after(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client2.likes(after=1418684291)
        assert response == []

    @mock.patch('requests.get')
    def test_likes_with_before(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client2.likes(before=1418684291)
        assert response == []

    @mock.patch('requests.get')
    def test_following(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client2.following()
        assert response == []

    @mock.patch('requests.get')
    def test_tagged(self, mock_get):
        mock_get.side_effect = wrap_response('{"meta": {"status": 200, "msg": "OK"}, "response": []}')

        response = self.client2.tagged('food')
        assert response == []

    @mock.patch('requests.post')
    def test_create_text(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client2.create_text('codingjester.tumblr.com', body="Testing")
        assert response == []

    @mock.patch('requests.post')
    def test_create_link(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 201, "msg": "OK"}, "response": []}',
            mock_post)

        response = self.client2.create_link('codingjester.tumblr.com', url="https://google.com", tags=['omg', 'nice'])
        assert response == []

        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('url=https%3A%2F%2Fgoogle.com&type=link&tags=omg%2Cnice')

    @mock.patch('requests.post')
    def test_no_tags(self, mock_post):
        mock_post.side_effect = wrap_response_storing_data(
            '{"meta": {"status": 201, "msg": "OK"}, "response": []}',
            mock_post)

        self.client2.create_link('seejohnrun.tumblr.com')
        assert parse_qs(urllib.parse.urlencode(mock_post.data)) == parse_qs('type=link&tags=')

    @mock.patch('requests.post')
    def test_create_quote(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client2.create_quote('codingjester.tumblr.com', quote="It's better to love and lost, than never have loved at all.")
        assert response == []

    @mock.patch('requests.post')
    def test_create_chat(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client2.create_chat('codingjester.tumblr.com', conversation="JB: Testing is rad.\nJC: Hell yeah.")
        assert response == []

    @mock.patch('requests.post')
    def test_create_photo(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client2.create_photo('codingjester.tumblr.com', source="https://media.tumblr.com/image.jpg")
        assert response == []

    @mock.patch('requests.post')
    def test_create_audio(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client2.create_audio('codingjester.tumblr.com', external_url="https://media.tumblr.com/audio.mp3")
        assert response == []

    @mock.patch('requests.post')
    def test_create_video(self, mock_post):
        mock_post.side_effect = wrap_response('{"meta": {"status": 201, "msg": "OK"}, "response": []}')

        response = self.client2.create_video('codingjester.tumblr.com', embed="blahblahembed")
        assert response == []

if __name__ == "__main__":
    unittest.main()
