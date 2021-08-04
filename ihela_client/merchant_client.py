"""
Pierre-Claver Koko Banywerha

UbuViz (c) 2019
info@ubuviz.com

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


iHela_BASE_URL = "http://192.168.4.1/"
iHela_BASE_TEST_URL = "https://testgate.ihela.online/"
iHela_TOKEN_URL = "oAuth2/token/"
iHela_AUTH_URL = "oAuth2/authorize/"


iHela_ENDPOINTS = {
    "USER_INFO": "api/v1/connected-user/",
    "BILL_INIT": "api/v1/payments/bill/init/",
    "BILL_VERIFY": "api/v1/payments/bill/verify/",
    "CASHIN": "api/v1/payments/cash-in/",
    "BANKS_ALL": "api/v1/bank/all",
}


class MerchantClient(object):
    def __init__(
        self, client_id, client_secret, state=None, prod=False, ihela_url=None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_object = None
        self.redirect_uri = None
        self.state = state
        self.prod_env = prod

        self.ihela_base_url = iHela_BASE_URL
        if self.prod_env == False:
            self.ihela_base_url = iHela_BASE_TEST_URL
        if self.prod_env == True:
            self.ihela_base_url = iHela_BASE_URL
        if ihela_url:
            self.ihela_base_url = iHela_BASE_TEST_URL

        self.authenticate()

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
                % (
                    self.auth_token_object["token_type"],
                    self.auth_token_object["access_token"],
                )
            }
        return {}

    def authenticate(self):
        url = iHela_TOKEN_URL
        auth_data = {"grant_type": "client_credentials"}

        if not self.prod_env:
            # TODO : Delete this line for production
            logger.debug(auth_data)

        auth_ = requests.post(
            self.get_url(url), auth=(self.client_id, self.client_secret), data=auth_data
        )
        self.auth_token_object = self.get_response(auth_)

        return auth_

    def is_authenticated(self):
        if isinstance(self.auth_token_object, dict) and self.auth_token_object.get(
            "access_token", None
        ):
            return True
        return False

    def get_access_token(self):
        if self.is_authenticated():
            return self.auth_token_object["access_token"]

    def get_token_type(self, code):
        if self.is_authenticated():
            return self.auth_token_object["token_type"]

    def init_bill(
        self,
        amount,
        user,
        description,
        reference,
        bank,
        bank_client_id,
        redirect_uri=None,
    ):
        if self.is_authenticated():
            bill_data = {
                "amount": amount,
                "description": description,
                "merchant_reference": reference,
                "user": user,
                "bank": bank,
                "bank_client_id": bank_client_id,
                "redirect_uri": redirect_uri,
            }
            url = iHela_ENDPOINTS["BILL_INIT"]
            bill_ = requests.post(
                self.get_url(url), data=bill_data, headers=self.get_auth_headers()
            )
            bill_initiated = self.get_response(bill_)

            return bill_initiated
        else:
            return {"errors": {"authentication": "The client is not authenticated"}}

    def verify_bill(self, code, reference):
        bill_data = {"code": code, "reference": reference}
        url = iHela_ENDPOINTS["BILL_VERIFY"]
        bill_ = requests.post(
            self.get_url(url), data=bill_data, headers=self.get_auth_headers()
        )
        bill_verified = self.get_response(bill_)

        return bill_verified

    def cashin_client(
        self, bank_slug, account, amount, merchant_reference, description
    ):
        cashin_data = {
            "bank_slug": bank_slug,
            "account": account,
            "amount": amount,
            "merchant_reference": merchant_reference,
            "description": description,
        }
        url = iHela_ENDPOINTS["CASHIN"]
        cashin_ = requests.post(
            self.get_url(url), data=cashin_data, headers=self.get_auth_headers()
        )
        cashin = self.get_response(cashin_)

        return cashin

    def get_bank_list(self):
        url = iHela_ENDPOINTS["BANKS_ALL"]
        banks_ = requests.get(self.get_url(url), headers=self.get_auth_headers())
        banks = self.get_response(banks_)

        return banks


if __name__ == "__main__":
    client_id = "4sS7OWlf8pqm04j1ZDtvUrEVSZjlLwtfGUMs2XWZ"
    client_secret = "HN7osYwSJuEOO4MEth6iNlBS8oHm7LBhC8fejkZkqDJUrvVQodKtO55bMr845kmplSlfK3nxFcEk2ryiXzs1UW1YfVP5Ed6Yw0RR6QmnwsQ7iNJfzTgeehZ2XM9mmhC3"

    cl = MerchantClient(client_id, client_secret, ihela_url="http://127.0.0.1:8080/")
    print("\nBILL INIT : ", cl.ihela_base_url)

    bill = cl.init_bill(
        2000, "pierreclaverkoko@gmail.com", "My description", secrets.token_hex(10)
    )

    if bill["bill"].get("merchant_reference"):
        print(bill)
        bill_verif = cl.verify_bill(
            bill["bill"]["merchant_reference"], bill["bill"]["code"]
        )

        print("\nBILL VERIFY : ", bill_verif)

    banks = cl.get_bank_list()

    print("\nBANKS : ", banks)

    cashin = cl.cashin_client(
        "MF1-0001", "000016-01", 20000, secrets.token_hex(10), "Cashin description"
    )

    print("\nCASHIN : ", cashin)
