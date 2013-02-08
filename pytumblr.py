import requests
import hmac
import time
import hashlib
import base64
import urllib

class TumblrRestClient(object):
    """
    A Python Client for the Tumblr API
    """

    def __init__(self, consumer_key, consumer_secret=None, oauth_token=None, oauth_secret=None, host="api.tumblr.com"):
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
        return self._get('/v2/user/likes', params)

    def following(self, params={}):
        return self._get('/v2/user/following', params)
    
    def dashboard(self, params={}):
        return self._get('/v2/user/dashboard', params)

    def tagged(self, tag, params={}):
        params.update({'tag' : tag, 'api_key' : self.credentials['consumer_key']})
        return self._get('/v2/tagged', params)

    def posts(self, blogname, params={}):
        url = '/v2/blog/%s/posts' % blogname
        params.update({'api_key': self.credentials['consumer_key']})
        return self._get(url,params)

    def blog_info(self, blogname, params={}):
        url = "/v2/blog/%s/info" % blogname
        params.update({'api_key' : self.credentials['consumer_key']})
        return self._get(url, params)
    
    def followers(self, blogname, params={}):
        url = "/v2/blog/%s/followers" % blogname
        return self._get(url, params)

    def blog_likes(self, blogname, params={}):
        url = "/v2/blog/%s/likes" % blogname
        params.update({'api_key' : self.credentials['consumer_key']})
        return self._get(url, params)
    
    def queue(self, blogname, params={}):
        url = "/v2/blog/%s/posts/queue" % blogname
        return self._get(url, params)

    def drafts(self, blogname, params={}):
        url = "/v2/blog/%s/posts/draft" % blogname
        return self._get(url, params)

    def submission(self, blogname, params={}):
        url = "/v2/blog/%s/posts/submission" % blogname
        return self._get(url, params)

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
        return requests.post('http://api.tumblr.com' + url, params=params, headers=header).json()
