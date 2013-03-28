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
client.edit(blogName, **params);

client.reblog(blogName, id, reblogkey);

client.deletePost(blogName, id);

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
### Tagged Methods

``` javascript
client.tagged(tag, **params);
```

## Running tests

``` bash
nosetests --with-coverage --cover-package=pytumblr
```
