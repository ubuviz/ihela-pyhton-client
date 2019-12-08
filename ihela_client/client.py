"""
Pierre-Claver Koko Banywerha

UbuViz (c) 2019

Python client for integration
"""

import logging, json, string
import urllib.parse

try:
    import secrets
except ImportError:  # Python < 3.6
    import random as secrets

import requests

logger = logging.getLogger(__name__)


iHela_BASE_URL = "https://gate.ihela.online/"
iHela_BASE_TEST_URL = "https://testgate.ihela.online/"
iHela_TOKEN_URL = "oAuth2/token/"
iHela_AUTH_URL = "oAuth2/authorize/"


iHela_ENDPOINTS = {"USER_INFO": "api/v1/user/"}


class Client(object):
    def __init__(self, client_id, client_secret, state=None, test=False, ihela_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_object = None
        self.user_object = None
        self.redirect_uri = None
        self.state = state

        self.ihela_base_url = iHela_BASE_URL
        if test:
            self.ihela_base_url = iHela_BASE_TEST_URL
        if ihela_url:
            self.ihela_base_url = ihela_url

    def get_response(self, resp):
        try:
            return resp.json()
        except json.decoder.JSONDecodeError:
            logger.error(resp.text)
            return None

    def get_url(self, url):
        return self.ihela_base_url + str(url)

    def get_auth_headers(self):
        return {
            "Authorization": "%s %s" % (self.auth_token_object["token_type"], self.auth_token_object["access_token"])
        }

    def get_authorization_url(self, redirect_uri, scope=None, response_type=None, state_=None):
        if not scope:
            scope = "read"

        if not response_type:
            response_type = "code"

        if not self.redirect_uri or self.redirect_uri != redirect_uri:
            self.redirect_uri = redirect_uri

        chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
        if not self.state:
            self.state = "".join(secrets.choice(chars) for _ in range(20))

        auth_parms = urllib.parse.urlencode(
            dict(
                scope=scope,
                state=self.state,  # Generate Random
                response_type=response_type,
                client_id=self.client_id,
                redirect_uri=urllib.parse.quote(redirect_uri),
            )
        )

        return requests.utils.requote_uri(self.get_url(iHela_AUTH_URL) + "?" + auth_parms)

    def authenticate(self, authorization_code, redirect_uri):
        url = iHela_AUTH_URL
        auth_ = requests.post(
            self.get_url(url),
            data={
                "grant_type": "authorization_code",
                "code": authorization_code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": redirect_uri,
                # "username": username,
                # "password": password,
            },
        )
        self.auth_token_object = self.get_response(auth_)

        self.get_user_info()

        return auth_

    # def get_access_token(self, code):
    #     data = {"redirect_uri": self.callback_url, "grant_type": "authorization_code", "code": code}
    #     if self.basic_auth:
    #         auth = requests.auth.HTTPBasicAuth(self.consumer_key, self.consumer_secret)
    #     else:
    #         auth = None
    #         data.update({"client_id": self.consumer_key, "client_secret": self.consumer_secret})
    #     params = None
    #     self._strip_empty_keys(data)
    #     url = self.access_token_url
    #     if self.access_token_method == "GET":
    #         params = data
    #         data = None
    #     # TODO: Proper exception handling
    #     resp = requests.request(
    #         self.access_token_method, url, params=params, data=data, headers=self.headers, auth=auth
    #     )

    #     access_token = None
    #     if resp.status_code in [200, 201]:
    #         # Weibo sends json via 'text/plain;charset=UTF-8'
    #         if resp.headers["content-type"].split(";")[0] == "application/json" or resp.text[:2] == '{"':
    #             access_token = resp.json()
    #         else:
    #             access_token = dict(parse_qsl(resp.text))
    #     if not access_token or "access_token" not in access_token:
    #         raise OAuth2Error("Error retrieving access token: %s" % resp.content)
    #     return access_token

    def is_authenticated(self):
        return self.auth_token_object is not None

    def get_user_info(self):
        if self.is_authenticated():
            url = iHela_ENDPOINTS["USER_INFO"]

            user_ = requests.get(self.get_url(url), headers=self.get_auth_headers())
            self.user_object = self.get_response(user_)

            return self.user_object
        return None


if __name__ == "__main__":
    client_id = "5Q3Ew1mQiZBd4UmI3W7LrfkJlLxA4T4lPIX3lnxx"
    client_secret = "9btvRN7VUsZMyCNddn1Zx1rIEUnX7ITsCH3YqgWRxfA0Za7aVHA2mlKnEU9m5Y7en3wQoAMDWBOqJ8QYVfFYnJmM8BYCB5tO9NIrkUOtDmvB3rYD0QyEWEFIsafqfx2J"

    cl = Client(client_id, client_secret, ihela_url="http://127.0.0.1:8080/")

    # cl.authenticate(username="pierre-claver-koko", password="pass123456")

    # print("Authenticated : ", cl.is_authenticated())
    # print("Token : ", cl.auth_token_object)
    # print("User : ", cl.user_object)

    url = cl.get_authorization_url("http://127.0.0.1:4040/")

    print(url)
