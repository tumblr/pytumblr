#!/usr/bin/python
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import input

import pytumblr
import yaml
import os
import code
from requests_oauthlib import OAuth2Session


def new_oauth(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print('Retrieve client id and client secret from https://www.tumblr.com/oauth/apps')
    client_id = input('Paste the client id here: ')
    client_secret = input('Paste the client secret here: ')
    redirect_uri = input('Paste the redirect uri here: ')
    scope = list(input('Enter scopes as a list: '))

    authorize_url = 'https://www.tumblr.com/oauth2/authorize'
    access_token_url = 'https://api.tumblr.com/v2/oauth2/token'

    oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    full_authorize_url, state = oauth_session.authorization_url(authorize_url)

    # Redirect to authentication page
    print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
    authorization_response = input('Allow then paste the full callback URL:\n')

    token = oauth_session.fetch_token(
        token_url=access_token_url,
        authorization_response=authorization_response,
        client_secret=client_secret
    )

    token_info = {
        'access_token': str(token.get('access_token')),
        'expires_in': str(token.get('expires_in')),
        'token_type': str(token.get('token_type')),
        'scope': [str(item) for item in token.get('scope')],
        'id_token': str(token.get('id_token')),
    }

    yaml_file = open(yaml_path, 'w+')
    yaml.dump(token_info, yaml_file, indent=2)
    yaml_file.close()

    return (token_info, client_id)

if __name__ == '__main__':
    yaml_path = os.path.expanduser('~') + '/.tumblr'

    if not os.path.exists(yaml_path):
        tokens, client_id = new_oauth(yaml_path)
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    print (tokens)

    # Haven't gotten creation of Client2 in this console to work yet

    # client = TumblrRestClient2(
    #     "q0JO2pw9kLtmiTDxYxch2oRpzkMwzkl6xK2WxlfPg84GT1267v",
    #     tokens
    # }
    #
    # print('pytumblr client created. You may run pytumblr commands prefixed with "client".\n')
    #
    # code.interact(local=dict(globals(), **{'client': client}))
