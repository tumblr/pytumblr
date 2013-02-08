import nose
import unittest
import pytumblr

class TumblrRestClientTest(unittest.TestCase):
    """
    """
    def setUp(self):
        self.client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def test_dashboard(self):
        response = self.client.dashboard()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    def test_posts(self):
        response = self.client.posts('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    def test_blogInfo(self):
        response = self.client.blog_info('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    def test_followers(self):
        response = self.client.followers('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    def test_blogLikes(self):
        response = self.client.blog_likes('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
        
        response = self.client.blog_likes('derekg.tumblr.com')
        print response
        assert response['meta']['status'] == 401
        assert response['meta']['msg'] == "Not Authorized"

    def test_queue(self):
        response = self.client.queue('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
    
    def test_drafts(self):
        response = self.client.drafts('codingjester.tumblr.com')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    def test_info(self):
        response = self.client.info()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
    
    def test_likes(self):
        response = self.client.likes()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    def test_following(self):
        response = self.client.following()
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"

    def test_tagged(self):
        response = self.client.tagged('food')
        assert response['meta']['status'] == 200
        assert response['meta']['msg'] == "OK"
        
        


if __name__ == "__main__":
    unittest.main()
