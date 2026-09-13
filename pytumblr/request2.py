from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import str

import urllib.parse

import requests
from requests.exceptions import TooManyRedirects


class TumblrRequest2(object):
    """HTTP transport for Tumblr OAuth 2 bearer-token requests."""

    __version = "0.1.3"
    TOKEN_URL = "https://api.tumblr.com/v2/oauth2/token"

    def __init__(self, client_id, token, client_secret="",
                 host="https://api.tumblr.com", timeout=30,
                 token_updater=None, allow_custom_host=False):
        self.host = self._validated_host(host, allow_custom_host)
        self.client_id = client_id
        self.consumer_key = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.token_updater = token_updater
        self.token = self._validated_token(token)
        self.headers = {"User-Agent": "pytumblr/" + self.__version}
        self._update_auth_header()

    @staticmethod
    def _validated_host(host, allow_custom_host=False):
        parsed = urllib.parse.urlsplit(host)
        if (parsed.scheme != "https" or not parsed.hostname or
                parsed.username or parsed.password or parsed.query or
                parsed.fragment or parsed.path not in ("", "/")):
            raise ValueError("OAuth2 host must be an HTTPS origin")
        origin = host.rstrip("/")
        if origin != "https://api.tumblr.com" and not allow_custom_host:
            raise ValueError("custom OAuth2 hosts require allow_custom_host=True")
        return origin

    @staticmethod
    def _validated_token(token):
        if not isinstance(token, dict) or not token.get("access_token"):
            raise ValueError("oauth2_token must contain an access_token")
        access_token = token["access_token"]
        token_type = token.get("token_type", "bearer")
        if not isinstance(access_token, str) or "\r" in access_token or "\n" in access_token:
            raise ValueError("OAuth2 access_token is invalid")
        if not isinstance(token_type, str) or token_type.lower() != "bearer":
            raise ValueError("Tumblr OAuth2 tokens must use the bearer token type")
        return dict(token)

    def _update_auth_header(self):
        self.headers["Authorization"] = "Bearer {}".format(
            self.token["access_token"]
        )

    def get(self, url, params):
        url = self.host + url
        if params:
            url += "?" + urllib.parse.urlencode(params)
        try:
            response = requests.get(
                url, allow_redirects=False, headers=self.headers,
                timeout=self.timeout
            )
        except TooManyRedirects as error:
            response = error.response
        return self.json_parse(response)

    def post(self, url, params=None, files=None):
        url = self.host + url
        params = params or {}
        files = files or {}
        if files:
            response = requests.post(
                url, data=params, files=files, headers=self.headers,
                allow_redirects=False, timeout=self.timeout
            )
        else:
            response = requests.post(
                url, data=params, headers=self.headers,
                allow_redirects=False, timeout=self.timeout
            )
        return self.json_parse(response)

    def delete(self, url, params):
        url = self.host + url
        if params:
            url += "?" + urllib.parse.urlencode(params)
        try:
            response = requests.delete(
                url, allow_redirects=False, headers=self.headers,
                timeout=self.timeout
            )
        except TooManyRedirects as error:
            response = error.response
        return self.json_parse(response)

    def refresh(self):
        if not self.client_secret:
            raise ValueError("client_secret is required to refresh an OAuth2 token")
        refresh_token = self.token.get("refresh_token")
        if not refresh_token:
            raise ValueError("oauth2_token does not contain a refresh_token")
        response = requests.post(
            self.TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={"User-Agent": "pytumblr/" + self.__version},
            allow_redirects=False,
            timeout=self.timeout,
        )
        try:
            payload = response.json()
        except ValueError:
            raise RuntimeError(
                "Tumblr OAuth2 refresh returned HTTP {} with invalid JSON".format(
                    response.status_code
                )
            )
        if not response.ok:
            description = payload.get("error_description") or payload.get("error")
            raise RuntimeError(
                "Tumblr OAuth2 refresh failed with HTTP {}: {}".format(
                    response.status_code, description or "unknown error"
                )
            )
        if "refresh_token" not in payload:
            payload["refresh_token"] = refresh_token
        self.token = self._validated_token(payload)
        self._update_auth_header()
        if self.token_updater is not None:
            self.token_updater(dict(self.token))
        return dict(self.token)

    def json_parse(self, response):
        try:
            data = response.json()
        except (ValueError, TypeError):
            data = {
                "meta": {"status": 500, "msg": "Server Error"},
                "response": {"error": "Malformed JSON or HTML was returned."},
            }
        meta = data.get("meta") if isinstance(data, dict) else None
        status = meta.get("status") if isinstance(meta, dict) else None
        if status is None:
            status = getattr(response, "status_code", 500)
        if 200 <= status <= 399 and isinstance(data, dict):
            return data.get("response", data)
        return data
