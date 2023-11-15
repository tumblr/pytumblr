#!/usr/bin/python
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import input

import pytumblr
import os
import code
from requests_oauthlib import OAuth1Session
try:
    import yaml
except ImportError:
    print('You need PyYAML to run interactive console\npip install pyyaml')
    import sys
    sys.exit(-1)


def new_oauth(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print('Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps')
    consumer_key = input('Paste the consumer key here: ').strip()
    consumer_secret = input('Paste the consumer secret here: ').strip()

    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    # STEP 1: Obtain request token
    oauth_session = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth_session.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    # STEP 2: Authorize URL + Response
    full_authorize_url = oauth_session.authorization_url(authorize_url)

    # Redirect to authentication page
    print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
    redirect_response = input('Allow then paste the full redirect URL here:\n').strip()

    # Retrieve oauth verifier
    oauth_response = oauth_session.parse_authorization_response(redirect_response)

    verifier = oauth_response.get('oauth_verifier')

    # STEP 3: Request final access token
    oauth_session = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier
    )
    oauth_tokens = oauth_session.fetch_access_token(access_token_url)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': oauth_tokens.get('oauth_token'),
        'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
    }

    yaml_file = open(yaml_path, 'w+')
    yaml.dump(tokens, yaml_file, indent=2)
    yaml_file.close()

    return tokens

if __name__ == '__main__':
    yaml_path = os.path.expanduser('~') + '/.tumblr'
    alternate_path = os.path.expanduser('~') + '/.pytumblr'

    if os.path.isdir(yaml_path) or os.path.exists(alternate_path):
        yaml_path = alternate_path

    if not os.path.exists(yaml_path):
        tokens = new_oauth(yaml_path)
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    client = pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )

    print('pytumblr client created. You may run pytumblr commands prefixed with "client".\n')

    code.interact(local=dict(globals(), **{'client': client}))
