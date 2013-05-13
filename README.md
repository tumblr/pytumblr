# PyTumblr

## Create a client

```python
client = pytumblr.TumblrRestClient(
    '<consumer_key>',
    '<consumer_secret>',
    '<oauth_token>',
    '<oauth_secret>',
)
```

## Example

```python
client.info() #Grabs the current user information
```

## Supported Methods

### User Methods

```python
client.info()
client.dashboard()
client.likes()
client.following()

client.follow('codingjester.tumblr.com')
client.unfollow('codingjester.tumblr.com')

client.like(id, reblogkey)
client.unlike(id, reblogkey)
```

### Blog Methods

```python
client.blog_info('codingjester')
client.posts('codingjester', **params)
client.avatar('codingjester')
client.blog_likes('codingjester')
client.followers('codingjester')
client.queue('codingjester')
client.submissions('codingjester')
```

### Post Methods

```python
client.edit_post(blogName, **params);

client.reblog(blogName, id, reblogkey);

client.delete_post(blogName, id);

client.create_photo(blogName, **params)
client.create_quote(blogName, **params)
client.create_text(blogName, **params)
client.create_link(blogName, **params)
client.create_chat(blogName, **params)
client.create_audio(blogName, **params)
client.create_video(blogName, **params)
```

### Tagged Methods

```python
client.tagged(tag, **params);
```

## Running tests

``` bash
nosetests --with-coverage --cover-package=pytumblr
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
