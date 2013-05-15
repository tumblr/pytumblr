from helpers import validate_params, validate_blogname
from request import TumblrRequest


class TumblrRestClient(object):
    """
    A Python Client for the Tumblr API
    """

    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret="", host="http://api.tumblr.com"):
        """
        Initializes the TumblrRestClient object, creating the TumblrRequest
        object which deals with all request formatting.

        :param consumer_key: a string, the consumer key of your
                             Tumblr Application
        :param consumer_secret: a string, the consumer secret of
                                your Tumblr Application
        :param oauth_token: a string, the user specific token, received
                            from the /access_token endpoint
        :param oauth_secret: a string, the user specific secret, received
                             from the /access_token endpoint
        :param host: the host that are you trying to send information to,
                     defaults to http://api.tumblr.com

        :returns: None
        """
        self.request = TumblrRequest(consumer_key, consumer_secret, oauth_token, oauth_secret, host)

    def info(self):
        """
        Gets the information about the current given user

        :returns: A dict created from the JSON response
        """
        return self.send_api_request("get", "/v2/user/info")

    @validate_blogname
    def avatar(self, blogname, size=64):
        """
        Retrieves the url of the blog's avatar
        
        :param blogname: a string, the blog you want the avatar for
        
        :returns: A dict created from the JSON response
        """
        url = "/v2/blog/%s/avatar/%d" % (blogname, size)
        return self.send_api_request("get", url)

    def likes(self, **kwargs):
        """
        Gets the current given user's likes
        :param limit: an int, the number of likes you want returned
        :param offset: an int, the like you want to start at, for pagination.

            # Start at the 20th like and get 20 more likes.
            client.likes({'offset': 20, 'limit': 20})

        :returns: A dict created from the JSON response
        """
        return self.send_api_request("get", "/v2/user/likes", kwargs, ["limit", "offset"])

    def following(self, **kwargs):
        """
        Gets the blogs that the current user is following.
        :param limit: an int, the number of likes you want returned
        :param offset: an int, the blog you want to start at, for pagination.

            # Start at the 20th blog and get 20 more blogs.
            client.following({'offset': 20, 'limit': 20})

        :returns: A dict created from the JSON response
        """
        return self.send_api_request("get", "/v2/user/following", kwargs, ["limit", "offset"])

    def dashboard(self, **kwargs):
        """
        Gets the dashboard of the current user

        :param limit: an int, the number of posts you want returned
        :param offset: an int, the posts you want to start at, for pagination.
        :param type:   the type of post you want to return
        :param since_id:  return only posts that have appeared after this ID
        :param reblog_info: return reblog information about posts
        :param notes_info:  return notes information about the posts

        :returns: A dict created from the JSON response
        """
        return self.send_api_request("get", "/v2/user/dashboard", kwargs, ["limit", "offset", "type", "since_id", "reblog_info", "notes_info"])

    def tagged(self, tag, **kwargs):
        """
        Gets a list of posts tagged with the given tag

        :param tag: a string, the tag you want to look for
        :param before: a unix timestamp, the timestamp you want to start at
                       to look at posts.
        :param limit: the number of results you want
        :param filter: the post format that you want returned: html, text, raw

            client.tagged("gif", limit=10)

        :returns: a dict created from the JSON response
        """
        kwargs.update({'tag': tag})
        return self.send_api_request("get", '/v2/tagged', kwargs, ['before', 'limit', 'filter', 'tag', 'api_key'], True)
    
    @validate_blogname
    def posts(self, blogname, **kwargs):
        """
        Gets a list of posts from a particular blog

        :param blogname: a string, the blogname you want to look up posts
                         for. eg: codingjester.tumblr.com
        :param id: an int, the id of the post you are looking for on the blog
        :param tag: a string, the tag you are looking for on posts
        :param limit: an int, the number of results you want
        :param offset: an int, the offset of the posts you want to start at.
        :param filter: the post format you want returned: HTML, text or raw.

        :returns: a dict created from the JSON response
        """
        url = '/v2/blog/%s/posts' % blogname
        return self.send_api_request("get", url, kwargs, ['id', 'tag', 'limit', 'offset', 'reblog_info', 'notes_info', 'filter', 'api_key'], True)
    
    @validate_blogname
    def blog_info(self, blogname):
        """
        Gets the information of the given blog

        :param blogname: the name of the blog you want to information
                         on. eg: codingjester.tumblr.com

        :returns: a dict created from the JSON response of information
        """
        url = "/v2/blog/%s/info" % blogname
        return self.send_api_request("get", url, {}, ['api_key'], True)
    
    @validate_blogname
    def followers(self, blogname, **kwargs):
        """
        Gets the followers of the given blog
        :param limit: an int, the number of followers you want returned
        :param offset: an int, the follower to start at, for pagination.

            # Start at the 20th blog and get 20 more blogs.
            client.followers({'offset': 20, 'limit': 20})

        :returns: A dict created from the JSON response
        """
        url = "/v2/blog/%s/followers" % blogname
        return self.send_api_request("get", url, kwargs, ['limit', 'offset'])
    
    @validate_blogname
    def blog_likes(self, blogname, **kwargs):
        """
        Gets the current given user's likes
        :param limit: an int, the number of likes you want returned
        :param offset: an int, the like you want to start at, for pagination.

            # Start at the 20th like and get 20 more likes.
            client.blog_likes({'offset': 20, 'limit': 20})

        :returns: A dict created from the JSON response
        """
        url = "/v2/blog/%s/likes" % blogname
        return self.send_api_request("get", url, kwargs, ['limit', 'offset'], True)
    
    @validate_blogname
    def queue(self, blogname, **kwargs):
        """
        Gets posts that are currently in the blog's queue

        :param limit: an int, the number of posts you want returned
        :param offset: an int, the post you want to start at, for pagination.
        :param filter: the post format that you want returned: HTML, text, raw.

        :returns: a dict created from the JSON response
        """
        url = "/v2/blog/%s/posts/queue" % blogname
        return self.send_api_request("get", url, kwargs, ['limit', 'offset', 'filter'])

    @validate_blogname
    def drafts(self, blogname, **kwargs):
        """
        Gets posts that are currently in the blog's drafts
        :param filter: the post format that you want returned: HTML, text, raw.

        :returns: a dict created from the JSON response
        """
        url = "/v2/blog/%s/posts/draft" % blogname
        return self.send_api_request("get", url, kwargs, ['filter'])

    @validate_blogname
    def submission(self, blogname, **kwargs):
        """
        Gets posts that are currently in the blog's queue

        :param offset: an int, the post you want to start at, for pagination.
        :param filter: the post format that you want returned: HTML, text, raw.

        :returns: a dict created from the JSON response
        """
        url = "/v2/blog/%s/posts/submission" % blogname
        return self.send_api_request("get", url, kwargs, ["offset", "filter"])

    @validate_blogname
    def follow(self, blogname):
        """
        Follow the url of the given blog

        :param blog_url: a string, the blog url you want to follow

        :returns: a dict created from the JSON response
        """
        url = "/v2/user/follow"
        return self.send_api_request("post", url, {'url': blogname}, ['url'])

    @validate_blogname
    def unfollow(self, blogname):
        """
        Unfollow the url of the given blog

        :param blog_url: a string, the blog url you want to follow

        :returns: a dict created from the JSON response
        """
        url = "/v2/user/unfollow"
        return self.send_api_request("post", url, {'url': blog_url}, ['url'])

    def like(self, id, reblog_key):
        """
        Like the post of the given blog

        :param id: an int, the id of the post you want to like
        :param reblog_key: a string, the reblog key of the post

        :returns: a dict created from the JSON response
        """
        url = "/v2/user/like"
        params = {'id': id, 'reblog_key': reblog_key}
        return self.send_api_request("post", url, params, ['id', 'reblog_key'])

    def unlike(self, id, reblog_key):
        """
        Unlike the post of the given blog

        :param id: an int, the id of the post you want to like
        :param reblog_key: a string, the reblog key of the post

        :returns: a dict created from the JSON response
        """
        url = "/v2/user/unlike"
        params = {'id': id, 'reblog_key': reblog_key}
        return self.send_api_request("post", url, params, ['id', 'reblog_key'])

    @validate_blogname
    def create_photo(self, blogname, **kwargs):
        """
        Create a photo post or photoset on a blog

        :param blogname: a string, the url of the blog you want to post to.
        :param state: a string, The state of the post.
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url
        :param caption: a string, the caption that you want applied to the photo
        :param link: a string, the 'click-through' url you want on the photo
        :param source: a string, the photo source url
        :param data: a string or a list of the path of photo(s)

        :returns: a dict created from the JSON response
        """
        kwargs.update({"type": "photo"})
        return self._send_post(blogname, kwargs, ['caption', 'link', 'source', 'type', 'data'])
    
    @validate_blogname
    def create_text(self, blogname, **kwargs):
        """
        Create a text post on a blog

        :param blogname: a string, the url of the blog you want to post to.
        :param state: a string, The state of the post.
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url
        :param title: a string, the optional title of a post
        :param body: a string, the body of the text post

        :returns: a dict created from the JSON response
        """
        kwargs.update({"type": "text"})
        return self._send_post(blogname, kwargs, ['text', 'title', 'body'])

    @validate_blogname
    def create_quote(self, blogname, **kwargs):
        """
        Create a quote post on a blog

        :param blogname: a string, the url of the blog you want to post to.
        :param state: a string, The state of the post.
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url
        :param quote: a string, the full text of the quote
        :param source: a string, the cited source of the quote

        :returns: a dict created from the JSON response
        """
        kwargs.update({"type": "quote"})
        return self._send_post(blogname, kwargs, ['quote', 'source'])

    @validate_blogname
    def create_link(self, blogname, **kwargs):
        """
        Create a link post on a blog

        :param blogname: a string, the url of the blog you want to post to.
        :param state: a string, The state of the post.
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url
        :param title: a string, the title of the link
        :param url: a string, the url of the link you are posting
        :param description: a string, the description of the link you are posting

        :returns: a dict created from the JSON response
        """
        kwargs.update({"type": "link"})
        return self._send_post(blogname, kwargs, ['title', 'url', 'description'])

    @validate_blogname
    def create_chat(self, blogname, **kwargs):
        """
        Create a chat post on a blog

        :param blogname: a string, the url of the blog you want to post to.
        :param state: a string, The state of the post.
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url
        :param title: a string, the title of the conversation
        :param converstaion: a string, the conversation you are posting

        :returns: a dict created from the JSON response
        """
        kwargs.update({"type": "chat"})
        return self._send_post(blogname, kwargs, ['title', 'conversation'])

    @validate_blogname
    def create_audio(self, blogname, **kwargs):
        """
        Create a audio post on a blog

        :param blogname: a string, the url of the blog you want to post to.
        :param state: a string, The state of the post.
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url
        :param caption: a string, the caption for the post
        :param external_url: a string, the url of the audio you are uploading
        :param data: a string, the local filename path of the audio you are uploading

        :returns: a dict created from the JSON response
        """
        kwargs.update({"type": "audio"})
        return self._send_post(blogname, kwargs, ['caption', 'external_url', 'data'])

    @validate_blogname
    def create_video(self, blogname, **kwargs):
        """
        Create a audio post on a blog

        :param blogname: a string, the url of the blog you want to post to.
        :param state: a string, The state of the post.
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url
        :param caption: a string, the caption for the post
        :param embed: a string, the emebed code that you'd like to upload
        :param data: a string, the local filename path of the video you are uploading

        :returns: a dict created from the JSON response
        """
        kwargs.update({"type": "video"})
        return self._send_post(blogname, kwargs, ['caption', 'embed', 'data'])

    @validate_blogname
    def reblog(self, blogname, **kwargs):
        """
        Creates a reblog on the given blogname

        :param blogname: a string, the url of the blog you want to reblog to
        :param id: an int, the post id that you are reblogging
        :param reblog_key: a string, the reblog key of the post

        :returns: a dict created from the JSON response
        """
        url = "/v2/blog/%s/post/reblog" % blogname
        return self.send_api_request('post', url, kwargs, ['id', 'reblog_key'])

    @validate_blogname
    def delete_post(self, blogname, id):
        """
        Deletes a post with the given id

        :param blogname: a string, the url of the blog you want to delete from
        :param id: an int, the post id that you want to delete

        :returns: a dict created from the JSON response
        """
        url = "/v2/blog/%s/post/delete" % blogname
        return self.send_api_request('post', url, {'id': id}, ['id'])

    @validate_blogname
    def edit_post(self, blogname, **kwargs):
        """
        Edits a post with a given id

        :param blogname: a string, the url of the blog you want to edit
        :param tags: a list of tags that you want applied to the post
        :param tweet: a string, the customized tweet that you want
        :param date: a string, the GMT date and time of the post
        :param format: a string, sets the format type of the post. html or markdown
        :param slug: a string, a short text summary to the end of the post url

        :returns: a dict created from the JSON response
        """
        url = "/v2/blog/%s/post/edit" % blogname
        return self.send_api_request('post', url, kwargs)

    def _send_post(self, blogname, params, valid_options):
        """
        Formats parameters and sends the API request off. Validates common parameters
        and formats your tags for you.

        :param blogname: a string, the blogname of the blog you are posting to
        :param params: a dict, the key-value of the parameters for the api request
        :param valid_options: a list of valid options that the request allows

        :returns: a dict parsed from the JSON response
        """
        url = "/v2/blog/%s/post" % blogname
        valid_options = ['type', 'state', 'tags', 'tweet', 'date', 'format', 'slug'] + valid_options

        if 'tags' in params:
            # Take a list of tags and make them acceptable for upload
            params['tags'] = ",".join(params['tags'])

        return self.send_api_request("post", url, params, valid_options)

    def send_api_request(self, method, url, params={}, valid_parameters=[], needs_api_key=False):
        """
        Sends the url with parameters to the requested url, validating them
        to make sure that they are what we expect to have passed to us

        :param method: a string, the request method you want to make
        :param params: a dict, the parameters used for the API request
        :param valid_parameters: a list, the list of valid parameters
        :param needs_api_key: a boolean, whether or not your request needs an api key injected

        :returns: a dict parsed from the JSON response
        """
        if needs_api_key:
            params.update({'api_key': self.request.consumer.key})
            valid_parameters.append('api_key')

        files = []
        if 'data' in params:
            if isinstance(params['data'], list):
                files = [('data['+str(idx)+']', data, open(data, 'rb').read()) for idx, data in enumerate(params['data'])]
            else:
                files = [('data', params['data'], open(params['data'], 'rb').read())]
            del params['data']

        validate_params(valid_parameters, params)
        if method == "get":
            return self.request.get(url, params)
        else:
            return self.request.post(url, params, files)
