"""
Pierre-Claver Koko Banywerha

UbuViz (c) 2019
info@ubuviz.com

Python client for integration
"""

import logging, json, string
import urllib.parse

__version__ = "0.0.2"

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


iHela_ENDPOINTS = {
    "USER_INFO": "api/v1/connected-user/",
    "BILL_INIT": "api/v1/payments/bill/init/",
    "BILL_VERIFY": "api/v1/payments/bill/verify/",
}


class Client(object):
    provider_name = "iHelá"

    def __init__(self, client_id, client_secret, state=None, test=False, ihela_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_object = None
        self.user_object = None
        self.redirect_uri = None
        self.state = state
        self.test_env = test

        self.ihela_base_url = iHela_BASE_URL
        if self.test_env:
            self.ihela_base_url = iHela_BASE_TEST_URL
        if ihela_url:
            self.ihela_base_url = ihela_url

    def get_response(self, resp):
        try:
            resp_json = dict(resp.json())
            resp_json["response_status"] = resp.status_code
            logger.debug(resp_json)
            return resp_json
        except json.decoder.JSONDecodeError:
            logger.error("IHELA_CLIENT_ERROR : %s" % resp.text)
            return {"errors": {"request": "An error occured during request"}}

    def get_url(self, url):
        return self.ihela_base_url + str(url)

    def get_auth_headers(self):
        if self.is_authenticated():
            return {
                "Authorization": "%s %s"
                % (self.auth_token_object["token_type"], self.auth_token_object["access_token"])
            }
        return {}

    def get_authorization_url(self, redirect_uri, state_=None):
        response_type = "code"

        if not self.redirect_uri or self.redirect_uri != redirect_uri:
            self.redirect_uri = redirect_uri

        chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
        if not self.state:
            self.state = "".join(secrets.choice(chars) for _ in range(20))

        auth_dict = dict(
            state=self.state,  # Generate Random
            response_type=response_type,
            client_id=self.client_id,
            redirect_uri=urllib.parse.quote(redirect_uri),
        )
        # auth_parms = urllib.parse.urlencode(auth_dict)
        auth_parms = "state={state}&response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}".format(
            **auth_dict
        )

        # return requests.utils.requote_uri(self.get_url(iHela_AUTH_URL) + "?" + auth_parms)
        return self.get_url(iHela_AUTH_URL) + "?" + auth_parms

    def authenticate(self, authorization_code, redirect_uri):
        url = iHela_TOKEN_URL
        auth_data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
            # "username": username,
            # "password": password,
        }

        if self.test_env:
            # TODO : Delete this line for production
            logger.debug(auth_data)

        auth_ = requests.post(self.get_url(url), data=auth_data)
        self.auth_token_object = self.get_response(auth_)

        self.get_user_info()

        return auth_

    def is_authenticated(self):
        if isinstance(self.auth_token_object, dict) and self.auth_token_object.get("access_token", None):
            return True
        return False

    def get_access_token(self):
        if self.is_authenticated():
            return self.auth_token_object["access_token"]

    def get_token_type(self, code):
        if self.is_authenticated():
            return self.auth_token_object["token_type"]

    def get_user_info(self):
        if self.is_authenticated():
            url = iHela_ENDPOINTS["USER_INFO"]

            user_ = requests.get(self.get_url(url), headers=self.get_auth_headers())
            self.user_object = self.get_response(user_)

            return self.user_object
        return None

    def bill_init(self, amount, description, reference, redirect_uri):
        if self.is_authenticated():
            bill_data = {
                "amount": amount,
                "description": description,
                "merchant_reference": reference,
                "redirect_uri": redirect_uri,
            }
            url = iHela_ENDPOINTS["BILL_INIT"]
            bill_ = requests.post(self.get_url(url), data=bill_data, headers=self.get_auth_headers())
            bill_initiated = self.get_response(bill_)

            return bill_initiated

            # TODO: Make further verifications to `bill_data` for better handling. e.g. amount type, max_lengths,...
            # TODO: Make try...except on requests.post to return other cool errors...
        else:
            return {"errors": {"authentication": "The client is not authenticated"}}

    def bill_verify(self, code, reference, intern_reference):
        bill_data = {"code": code, "reference": reference, "intern_reference": intern_reference}
        url = iHela_ENDPOINTS["BILL_VERIFY"]
        bill_ = requests.post(self.get_url(url), data=bill_data)
        bill_verified = self.get_response(bill_)

        return bill_verified


if __name__ == "__main__":
    client_id = "5Q3Ew1mQiZBd4UmI3W7LrfkJlLxA4T4lPIX3lnxx"
    client_secret = "9btvRN7VUsZMyCNddn1Zx1rIEUnX7ITsCH3YqgWRxfA0Za7aVHA2mlKnEU9m5Y7en3wQoAMDWBOqJ8QYVfFYnJmM8BYCB5tO9NIrkUOtDmvB3rYD0QyEWEFIsafqfx2J"

    cl = Client(client_id, client_secret, ihela_url="http://127.0.0.1:8080/")
    url = cl.get_authorization_url("http://127.0.0.1:4040/")

    print(url)
