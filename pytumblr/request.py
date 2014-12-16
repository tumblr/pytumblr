import urllib
import urllib2
import time
import json

from urlparse import parse_qsl
import oauth2 as oauth
from httplib2 import RedirectLimit

class TumblrRequest(object):
    """
    A simple request object that lets us query the Tumblr API
    """

    __version = "0.0.7";

    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="", host="https://api.tumblr.com"):
        self.host = host
        self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        self.token = oauth.Token(key=oauth_token, secret=oauth_secret)
        self.headers = {
            "User-Agent" : "pytumblr/" + self.__version
        }

    def get(self, url, params):
        """
        Issues a GET request against the API, properly formatting the params

        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the paramaters needed
                       in the request
        :returns: a dict parsed of the JSON response
        """
        url = self.host + url
        if params:
            url = url + "?" + urllib.urlencode(params)

        client = oauth.Client(self.consumer, self.token)
        try:
            client.follow_redirects = False
            resp, content = client.request(url, method="GET", redirections=False, headers=self.headers)
        except RedirectLimit, e:
            resp, content = e.args

        return self.json_parse(content)

    def post(self, url, params={}, files=[]):
        """
        Issues a POST request against the API, allows for multipart data uploads

        :param url: a string, the url you are requesting
        :param params: a dict, the key-value of all the parameters needed
                       in the request
        :param files: a list, the list of tuples of files

        :returns: a dict parsed of the JSON response
        """
        url = self.host + url
        try:
            if files:
                return self.post_multipart(url, params, files)
            else:
                client = oauth.Client(self.consumer, self.token)
                resp, content = client.request(url, method="POST", body=urllib.urlencode(params), headers=self.headers)
                return self.json_parse(content)
        except urllib2.HTTPError, e:
            return self.json_parse(e.read())

    def json_parse(self, content):
        """
        Wraps and abstracts content validation and JSON parsing
        to make sure the user gets the correct response.
        
        :param content: The content returned from the web request to be parsed as json
        
        :returns: a dict of the json response
        """
        try:
            data = json.loads(content)
        except ValueError, e:
            data = {'meta': { 'status': 500, 'msg': 'Server Error'}, 'response': {"error": "Malformed JSON or HTML was returned."}}
        
        #We only really care about the response if we succeed
        #and the error if we fail
        if data['meta']['status'] in [200, 201, 301]:
            return data['response']
        else:
            return data

    def post_multipart(self, url, params, files):
        """
        Generates and issues a multipart request for data files

        :param url: a string, the url you are requesting
        :param params: a dict, a key-value of all the parameters
        :param files:  a list, the list of tuples for your data

        :returns: a dict parsed from the JSON response
        """
        #combine the parameters with the generated oauth params
        params = dict(params.items() + self.generate_oauth_params().items())
        faux_req = oauth.Request(method="POST", url=url, parameters=params)
        faux_req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        params = dict(parse_qsl(faux_req.to_postdata()))

        content_type, body = self.encode_multipart_formdata(params, files)
        headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}

        #Do a bytearray of the body and everything seems ok
        r = urllib2.Request(url, bytearray(body), headers)
        content = urllib2.urlopen(r).read()
        return self.json_parse(content)

    def encode_multipart_formdata(self, fields, files):
        """
        Properly encodes the multipart body of the request

        :param fields: a dict, the parameters used in the request
        :param files:  a list of tuples containing information about the files

        :returns: the content for the body and the content-type value
        """
        import mimetools
        import mimetypes
        BOUNDARY = mimetools.choose_boundary()
        CRLF = '\r\n'
        L = []
        for (key, value) in fields.items():
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="{0}"'.format(key))
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(key, filename))
            L.append('Content-Type: {0}'.format(mimetypes.guess_type(filename)[0] or 'application/octet-stream'))
            L.append('Content-Transfer-Encoding: binary')
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary={0}'.format(BOUNDARY)
        return content_type, body

    def generate_oauth_params(self):
        """
        Generates the oauth parameters needed for multipart/form requests

        :returns: a dictionary of the proper headers that can be used
                  in the request
        """
        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_token': self.token.key,
            'oauth_consumer_key': self.consumer.key
        }
        return params
