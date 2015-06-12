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

#### Creating posts

PyTumblr lets you create all of the various types that Tumblr supports. When using
these types there are a few defaults that are able to be used with any post type. 

The default supported types are described below.

* **state**  - a string, the state of the post. Supported types are _published_, _draft_, _queue_, _private_
* **tags**   - a list, a list of strings that you want tagged on the post. eg: ["testing", "magic", "1"]
* **tweet**  - a string, the string of the customized tweet you want. eg: "Man I love my mega awesome post!"
* **date**   -  a string, the customized GMT that you want
* **format** - a string, the format that your post is in. Support types are _html_ or _markdown_
* **slug**   - a string, the slug for the url of the post you want

We'll show examples throughout of these default examples while showcasing all the specific post types.

##### Creating a photo post

Creating a photo post supports a bunch of different options plus the described default options
* **caption** - a string, the user supplied caption
* **link**    - a string, the "click-through" url for the photo
* **source**  - a string, the url for the photo you want to use (use this or the data parameter)
* **data**    - a list or string, a list of filepaths or a single file path for multipart file upload

```python
#Creates a photo post using a source URL
client.create_photo('codingjester', state="published", tags=["testing", "ok"], source="https://36.media.tumblr.com/b965fbb2e501610a29d80ffb6fb3e1ad/tumblr_n55vdeTse11rn1906o1_500.jpg")

#Creates a photo post using a local filepath
client.create_photo('codingjester', state="queue", tags=["testing", "ok"], tweet="Woah this is an incredible sweet post [URL]", data="/Users/johnb/path/to/my/image.jpg")

#Creates a photoset post using several local filepaths
client.create_photo('codingjester', state="draft", tags=["jb is cool"], format="markdown", data=["/Users/johnb/path/to/my/image.jpg", "/Users/johnb/Pictures/kittens.jpg"], caption="## Mega sweet kittens")
```

##### Creating a text post

Creating a text post supports the same options as default and just a two other parameters
* **title** - a string, the optional title for the post. Supports markdown or html
* **body**  - a string, the body of the of the post. Supports markdown or html

```python
#Creating a text post
client.create_text("codingjester", state="published", slug="testing-text-posts", title="Testing", body="testing1 2 3 4")
```

#####  Creating a quote post
Creating a quote post supports the same options as default and two other parameter
* **quote**  - a string, the full text of the qote. Supports markdown or html
* **source** - a string, the cited source. HTML supported

```python
#Creating a quote post
client.create_quote("codingjester", state="queue", quote="I am the Walrus", source="Ringo")
```

##### Creating a link post
* **title**       - a string, the title of post that you want. Supports HTML entities. 
* **url**         - a string, the url that you want to create a link post for. 
* **description** - a string, the desciption of the link that you have

```python
#Create a link post
client.create_link('codingjester', title="I like to search things, you should too.", url="https://duckduckgo.com", description="Search is pretty cool when a duck does it.")
```

##### Creating a chat post
Creating a chat post supports the same options as default and two other parameters
* **title**        - a string, the title of the chat post
* **conversation** - a string, the text of the conversation/chat, with diablog labels (no html)

```python
#Create a chat post
chat = """John: Testing can be fun!
Renee: Testing is tedious and so are you.
John: Aw.
"""
client.create_chat('codingjester', title="Renee just doesn't understand.", conversation=chat, tags=["renee", "testing"])
```

##### Creating an audio post
Creating an audio post allows for all default options and a has 3 other parameters. The only thing to keep
in mind while dealing with audio posts is to make sure that you use the external_url parameter or data. You
cannot use both at the same time.
* **caption**      - a string, the caption for your post
* **external_url** - a string, the url of the site that hosts the audio file
* **data**         - a string, the filepath of the audio file you want to upload to Tumblr
```python
#Creating an audio file
client.create_audio('codingjester', caption="Rock out.", data="/Users/johnb/Music/my/new/sweet/album.mp3")

#lets use soundcloud!
client.create_audio('codingjester', caption="Mega rock out.", external_url="https://soundcloud.com/skrillex/sets/recess")
```

##### Creating a video post
Creating a video post allows for all default options and has three other options. Like the other post types,
it has some restrictions. You cannot use the embed and data parameters at the same time.
* **caption**     - a string, the caption for your post
* **embed**       - a string, the HTML embed code for the video
* **data**        - a string, the path of the file you want to upload

```python
#Creating an upload from YouTube
client.create_video('codingjester', caption="Jon Snow. Mega ridiculous sword.", embed="http://www.youtube.com/watch?v=40pUYLacrj4")

#Creating a video post from local file
client.create_video('codingjester', caption="testing", data="/Users/johnb/testing/ok/blah.mov")
```

#### Editing a post
Updating a post requires you knowing what type a post you're updating. You'll be able to supply to the post
any of the options given above for updates.

``` python
client.edit_post(blogName, title="OK", data="/Users/johnb/mega/awesome.jpg"); # edit a post
```

#### Reblogging a Post
Reblogging a post just requires knowing the post id and the reblog key, which is supplied in the JSON of any post object.

```python
client.reblog("codingjester", 125356, "reblog_key")
```

#### Deleting a post
Deleting just requires that you own the post and have the post id
```python
client.delete_post("codingjester", 123456) # Deletes your post :(
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
