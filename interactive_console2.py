#!/usr/bin/python
from __future__ import print_function

from builtins import input
from future import standard_library
standard_library.install_aliases()

import code
import getpass
import hmac
import os
import urllib.parse

from requests_oauthlib import OAuth2Session

import pytumblr

try:
    import yaml
except ImportError:
    print('You need PyYAML to run interactive console 2\npip install pyyaml')
    raise SystemExit(-1)

from pytumblr.credentials import load_credentials, save_credentials


AUTHORIZE_URL = 'https://www.tumblr.com/oauth2/authorize'
TOKEN_URL = 'https://api.tumblr.com/v2/oauth2/token'


def validate_authorization_response(redirect_uri, response_url, expected_state):
    expected = urllib.parse.urlsplit(redirect_uri)
    response = urllib.parse.urlsplit(response_url)
    expected_target = (
        expected.scheme.lower(), expected.hostname, expected.port, expected.path
    )
    response_target = (
        response.scheme.lower(), response.hostname, response.port, response.path
    )
    if expected_target != response_target:
        raise ValueError("OAuth2 response does not match the registered redirect URI")
    query = urllib.parse.parse_qs(response.query)
    response_states = query.get('state', [])
    codes = query.get('code', [])
    if (len(response_states) != 1 or
            not hmac.compare_digest(str(response_states[0]), str(expected_state))):
        raise ValueError("OAuth2 state validation failed")
    if len(codes) != 1 or not codes[0]:
        raise ValueError("OAuth2 response does not contain one authorization code")


def new_oauth2(yaml_path):
    client_id = input('Paste the OAuth consumer key here: ').strip()
    client_secret = getpass.getpass(
        'Paste the OAuth consumer secret here: '
    ).strip()
    redirect_uri = input('Paste the registered OAuth2 redirect URI here: ').strip()
    scope = input('Scopes [basic]: ').strip()
    scope = scope or 'basic'

    oauth_session = OAuth2Session(
        client_id, redirect_uri=redirect_uri, scope=scope.split()
    )
    authorization_url, state = oauth_session.authorization_url(
        AUTHORIZE_URL, response_type='code'
    )
    print('\nPlease go here and authorize:\n{}'.format(authorization_url))
    redirect_response = input(
        'After authorization, paste the full redirect URL here:\n'
    ).strip()
    validate_authorization_response(redirect_uri, redirect_response, state)
    token = oauth_session.fetch_token(
        TOKEN_URL,
        authorization_response=redirect_response,
        client_secret=client_secret,
        include_client_id=True,
        timeout=30,
    )

    tokens = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'token': token,
    }
    save_credentials(yaml_path, tokens)
    return tokens


if __name__ == '__main__':
    yaml_path = os.path.expanduser('~/.pytumblr-oauth2')
    if not os.path.exists(yaml_path):
        credentials = new_oauth2(yaml_path)
    else:
        credentials = load_credentials(yaml_path)

    def persist_token(token):
        credentials['token'] = token
        save_credentials(yaml_path, credentials)

    client = pytumblr.TumblrRestClient2(
        credentials['client_id'],
        credentials['token'],
        client_secret=credentials['client_secret'],
        token_updater=persist_token,
    )
    print('\npytumblr OAuth2 client created. Run commands prefixed with "client".\n')
    code.interact(local=dict(globals(), **{'client': client}))
