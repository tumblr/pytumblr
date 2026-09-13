import unittest

from mock import Mock, patch

import pytumblr


TOKEN = {
    "access_token": "access-token",
    "refresh_token": "refresh-token",
    "token_type": "bearer",
    "expires_in": 2520,
    "scope": "basic write offline_access",
}


def response(status, payload):
    result = Mock()
    result.status_code = status
    result.ok = status < 400
    result.json.return_value = payload
    return result


class OAuth2ClientTests(unittest.TestCase):

    @patch("pytumblr.request2.requests.get")
    def test_oauth2_client_uses_bearer_header(self, get):
        get.return_value = response(
            200, {"meta": {"status": 200}, "response": {"user": {}}}
        )
        client = pytumblr.TumblrRestClient2("client-id", TOKEN)
        self.assertEqual(client.info(), {"user": {}})
        self.assertEqual(
            get.call_args[1]["headers"]["Authorization"],
            "Bearer access-token",
        )
        self.assertFalse(get.call_args[1]["allow_redirects"])
        self.assertEqual(get.call_args[1]["timeout"], 30)

    @patch("pytumblr.request2.requests.get")
    def test_oauth2_public_endpoint_uses_client_id_as_api_key(self, get):
        get.return_value = response(
            200, {"meta": {"status": 200}, "response": {}}
        )
        pytumblr.TumblrRestClient2(
            "client-id", TOKEN
        ).blog_info("example.tumblr.com")
        self.assertIn("api_key=client-id", get.call_args[0][0])

    @patch("pytumblr.request2.requests.post")
    def test_oauth2_refresh_replaces_tokens_and_notifies_updater(self, post):
        replacement = dict(
            TOKEN, access_token="new-access", refresh_token="new-refresh"
        )
        post.return_value = response(200, replacement)
        updater = Mock()
        client = pytumblr.TumblrRestClient2(
            "client-id",
            TOKEN,
            client_secret="client-secret",
            token_updater=updater,
        )
        self.assertEqual(client.refresh_token(), replacement)
        self.assertEqual(
            client.request.headers["Authorization"], "Bearer new-access"
        )
        body = post.call_args[1]["data"]
        self.assertEqual(body["grant_type"], "refresh_token")
        self.assertEqual(body["refresh_token"], "refresh-token")
        self.assertEqual(
            post.call_args[0][0],
            "https://api.tumblr.com/v2/oauth2/token",
        )
        self.assertFalse(post.call_args[1]["allow_redirects"])
        updater.assert_called_once_with(replacement)

    @patch("pytumblr.request2.requests.post")
    def test_refresh_preserves_refresh_token_and_rejects_bad_replacement(
            self, post):
        post.return_value = response(
            200, {"access_token": "new-access", "token_type": "bearer"}
        )
        client = pytumblr.TumblrRestClient2(
            "client-id", TOKEN, client_secret="client-secret"
        )
        self.assertEqual(
            client.refresh_token()["refresh_token"], "refresh-token"
        )
        post.return_value = response(200, {"access_token": "bad\nvalue"})
        with self.assertRaises(ValueError):
            client.refresh_token()
        self.assertEqual(client.request.token["access_token"], "new-access")

    @patch("pytumblr.request2.requests.post")
    def test_refresh_error_does_not_expose_response_secrets(self, post):
        post.return_value = response(
            400,
            {"error": "invalid_grant", "access_token": "server-secret"},
        )
        client = pytumblr.TumblrRestClient2(
            "client-id", TOKEN, client_secret="client-secret"
        )
        with self.assertRaises(RuntimeError) as error:
            client.refresh_token()
        self.assertIn("invalid_grant", str(error.exception))
        self.assertNotIn("server-secret", str(error.exception))

    def test_oauth2_rejects_access_tokens_with_newlines(self):
        with self.assertRaises(ValueError):
            pytumblr.TumblrRestClient2(
                "client-id",
                {"access_token": "bad\nheader", "token_type": "bearer"},
            )

    def test_oauth2_rejects_non_bearer_token_type(self):
        with self.assertRaises(ValueError):
            pytumblr.TumblrRestClient2(
                "client-id",
                {"access_token": "token", "token_type": "mac"},
            )

    def test_oauth2_rejects_insecure_or_unapproved_hosts(self):
        with self.assertRaises(ValueError):
            pytumblr.TumblrRestClient2(
                "client-id", TOKEN, host="http://api.tumblr.com"
            )
        with self.assertRaises(ValueError):
            pytumblr.TumblrRestClient2(
                "client-id", TOKEN, host="https://example.com"
            )
        client = pytumblr.TumblrRestClient2(
            "client-id",
            TOKEN,
            host="https://example.com",
            allow_custom_host=True,
        )
        self.assertEqual(client.request.host, "https://example.com")

    def test_oauth1_preserves_custom_host_compatibility(self):
        client = pytumblr.TumblrRestClient(
            "consumer-key", host="http://localhost:8080"
        )
        self.assertEqual(client.request.host, "http://localhost:8080")
