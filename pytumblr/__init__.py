import requests
import hmac
import time
import hashlib
import base64
import urllib
from helpers import validate_params

valid_post_options = ['type', 'state', 'tags', 'tweet', 'date', 'format', 'slug']

class TumblrRestClient(object):
    """
    A Python Client for the Tumblr API
    """

    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="", host="api.tumblr.com"):
        """
        """
        self.host = host
        self.credentials = {
            'consumer_key' : consumer_key,
            'consumer_secret' : consumer_secret,
            'oauth_token' : oauth_token,
            'oauth_secret' : oauth_secret
        }

    def info(self):
        return self._get('/v2/user/info')
    
    def likes(self, params={}):
        validate_params(['limit', 'offset'], params)
        return self._get('/v2/user/likes', params)
    
    def following(self, params={}):
        validate_params(['limit', 'offset'], params)
        return self._get('/v2/user/following', params)
    
    def dashboard(self, params={}):
        validate_params(['limit', 'offset', 'type', 'since_id', 'reblog_info', 'notes_info'], params)
        return self._get('/v2/user/dashboard', params)

    def tagged(self, tag, params={}):
        validate_params(['before', 'limit', 'filter'], params)
        params.update({'tag' : tag, 'api_key' : self.credentials['consumer_key']})
        return self._get('/v2/tagged', params)

    def posts(self, blogname, params={}):
        url = '/v2/blog/%s/posts' % blogname
        validate_params(["id", "tag", "limit", "offset", "reblog_info", "notes_info", "filter"], params)
        params.update({'api_key': self.credentials['consumer_key']})
        return self._get(url, params)
    
    def blog_info(self, blogname):
        url = "/v2/blog/%s/info" % blogname
        return self._get(url, {'api_key' : self.credentials['consumer_key']})

    def followers(self, blogname, params={}):
        url = "/v2/blog/%s/followers" % blogname
        validate_params(['limit', 'offset'], params)
        return self._get(url, params)
    
    def blog_likes(self, blogname, params={}):
        url = "/v2/blog/%s/likes" % blogname
        validate_params(['limit', 'offset'], params)
        params.update({'api_key' : self.credentials['consumer_key']})
        return self._get(url, dict(params))

    def queue(self, blogname, params={}):
        url = "/v2/blog/%s/posts/queue" % blogname
        validate_params(['limit', 'offset', 'filter'], params)
        return self._get(url, params)

    def drafts(self, blogname, params={}):
        url = "/v2/blog/%s/posts/draft" % blogname
        validate_params(['filter'], params)
        return self._get(url, params)
    
    def submission(self, blogname, params={}):
        url = "/v2/blog/%s/posts/submission" % blogname
        validate_params(["offset", "filter"], params)
        return self._get(url, params)

    def follow(self, blogname):
        url = "/v2/blog/user/follow"
        params = {'url' : blogname}
        return self._post(url, params)
    
    def unfollow(self, blogname):
        url = "/v2/blog/user/unfollow"
        params = {'url' : blogname}
        return self._post(url, params)

    def like(self, params={}):
        url = "/v2/user/like"
        validate_params(['id', 'reblog_key'], params)
        return self._post(url, params)
    
    def unlike(self, params={}):
        url = "/v2/user/unlike"
        validate_params(['id', 'reblog_key'], params)
        return self._post(url, params)

    def post_photo(self, blogname, params={}):
        params.update({"type" : "photo"})
        valid_options = valid_post_options + ['caption', 'link', 'source', 'data', 'type']
        validate_params(valid_options, params)
        return self._send_post(blogname, params, valid_options)

    def post_text(self, blogname, params={}):
        params.update({"type" : "text"})
        valid_options = valid_post_options + ['text', 'body']
        validate_params(valid_options, params)
        return self._send_post(blogname, params, valid_options)
    
    def post_quote(self, blogname, params={}):
        params.update({"type" : "quote"})
        valid_options = valid_post_options + ['quote', 'source']
        validate_params(valid_options, params)
        return self._send_post(blogname, params, valid_options)

    def post_link(self, blogname, params={}):
        params.update({"type" : "link"}
        valid_options = valid_post_options + ['title', 'url', 'description']
        validate_params(valid_options, params)
        return self._send_post(blogname, params, valid_options)

    def post_chat(self, blogname, params={}):
        params.update({"type" : "chat"}
        valid_options = valid_post_options + ['title', 'conversation']
        validate_params(valid_options, params)
        return self._send_post(blogname, params, valid_options)

    def post_audio(self, blogname, params={}):
        params.update({"type" : "audio"}
        valid_options = valid_post_options + ['caption', 'external_url', 'data']
        validate_params(valid_options, params)
        return self._send_post(blogname, params, valid_options)

    def post_video(self, blogname, params={}):
        params.update({"type" : "video"}
        valid_options = valid_post_options + ['caption', 'embed', 'data']
        validate_params(valid_options, params)
        return self._send_post(blogname, params, valid_options)
    
    def _send_post(blogname, params, valid_options):
        url = "/v2/blog/%s/posts" % blogname
        return self._post(url, params)

    def oauth_header_gen(self, method, url, params):
        """
        """
        sig_params = dict([(x[0], urllib.quote(str(x[1])).replace('/','%2F')) for x in params.iteritems()])
        sig_params['oauth_consumer_key'] = self.credentials['consumer_key']
        sig_params['oauth_nonce'] = str(time.time())[::-1]
        sig_params['oauth_signature_method'] = 'HMAC-SHA1'
        sig_params['oauth_timestamp'] = str(int(time.time()))
        sig_params['oauth_version'] = '1.0'
        sig_params['oauth_token']= self.credentials['oauth_token']
        sig_params['oauth_signature'] = self.oauth_sig(method,'http://'+self.host + url, sig_params)
        return  'OAuth ' + ',  '.join(['%s="%s"' %(k,v) for k,v in sig_params.iteritems() if 'oauth' in k ])

    def oauth_sig(self, method, url, params):
        """
        """
        #eg: POST&http%3A%2F%2Fapi.tumblr.com%2Fv2%2Fblog%2Fexample.tumblr.com%2Fpost
        s = method + '&'+ urllib.quote(url).replace('/','%2F')+ '&' + '%26'.join(
            #escapes all the key parameters, we then strip and url encode these guys
            [urllib.quote(k) +'%3D'+ urllib.quote(params[k]).replace('/','%2F') for k in sorted(params.keys())]
        )
        s = s.replace('%257E','~')
        return urllib.quote(base64.encodestring(hmac.new(self.credentials['consumer_secret'] +"&"+self.credentials['oauth_secret'],s,hashlib.sha1).digest()).strip()) 
    
    def _get(self, url, params={}):
        auth_header = self.oauth_header_gen("GET", url, params)
        header = {'Authorization' : auth_header, "Content-type": 'application/x-www-form-urlencoded'}
        return requests.get('http://api.tumblr.com' + url, params=params, headers=header).json()

    def _post(self, url, params={}):
        auth_header = self.oauth_header_gen("POST", url, params)
        header = {'Authorization' : auth_header, "Content-type": 'application/x-www-form-urlencoded'}
        return requests.post('http://api.tumblr.com' + url, data=params, headers=header).json()
