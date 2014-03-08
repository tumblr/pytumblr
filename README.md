# PyTumblr

[![Build Status](https://travis-ci.org/tumblr/pytumblr.png?branch=master)](https://travis-ci.org/tumblr/pytumblr)

## Create a client

A `pytumblr.TumblrRestClient` is the object you'll make all of your calls to the
Tumblr API through.  Creating one is this easy:

``` python
client = pytumblr.TumblrRestClient(
    '<consumer_key>',
    '<consumer_secret>',
    '<oauth_token>',
    '<oauth_secret>',
)

client.info() # Grabs the current user information
```

Two easy ways to get your credentials to are:

1.  The built-in `interactive_console.py` tool (if you already have a consumer key & secret)
2.  The Tumblr API console at https://api.tumblr.com/console

## Supported Methods

### User Methods

``` python
client.info() # get information about the authenticating user
client.dashboard() # get the dashboard for the authenticating user
client.likes() # get the likes for the authenticating user
client.following() # get the blogs followed by the authenticating user

client.follow('codingjester.tumblr.com') # follow a blog
client.unfollow('codingjester.tumblr.com') # unfollow a blog

client.like(id, reblogkey) # like a post
client.unlike(id, reblogkey) # unlike a post
```

### Blog Methods

``` python
client.blog_info('codingjester') # get information about a blog
client.posts('codingjester', **params) # get posts for a blog
client.avatar('codingjester') # get the avatar for a blog
client.blog_likes('codingjester') # get the likes on a blog
client.followers('codingjester') # get the followers of a blog
client.queue('codingjester') # get the queue for a given blog
client.submission('codingjester') # get the submissions for a given blog
```

### Post Methods

``` python
client.edit_post(blogName, **params); # edit a post

client.reblog(blogName, id, reblogkey); # reblog a post

client.delete_post(blogName, id); # delete a post

# some helper methods for creating posts of varying types
client.create_photo(blogName, **params)
client.create_quote(blogName, **params)
client.create_text(blogName, **params)
client.create_link(blogName, **params)
client.create_chat(blogName, **params)
client.create_audio(blogName, **params)
client.create_video(blogName, **params)
```

A note on tags: When passing tags, as params, please pass them as a list (not
a comma-separated string):

``` python
client.create_text('seejohnrun', tags=['hello', 'world'], ...)
```

### Tagged Methods

```python
client.tagged(tag, **params); # get posts with a given tag
```

## Using the interactive console

This client comes with a nice interactive console to run you through the OAuth
process, grab your tokens (and store them for future use).

You'll need `pyyaml` installed to run it, but then it's just:

``` bash
$ python interactive-console.py
```

and away you go!  Tokens are stored in `~/.tumblr` and are also shared by other
Tumblr API clients like the Ruby client.

## Running tests

The tests (and coverage reports) are run with nose, like this:

``` bash
python setup.py test
```

# Copyright and license

Copyright 2013 Tumblr, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this work except in compliance with the License. You may obtain a copy of
the License in the LICENSE file, or at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations.
