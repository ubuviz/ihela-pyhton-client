"""
Pierre-Claver Koko Banywerha

UbuViz (c) 2019
info@ubuviz.com

Python client for integration
"""

import logging, json, string
import simplejson
import urllib.parse


try:
    import secrets
except ImportError:  # Python < 3.6
    import random as secrets

import requests

logger = logging.getLogger(__name__)


iHela_BASE_URL = "https://api.ihela.bi/"
iHela_BASE_TEST_URL = "https://testapi.ihela.bi/"
iHela_TOKEN_URL = "oAuth2/token/"
iHela_AUTH_URL = "oAuth2/authorize/"


iHela_ENDPOINTS = {
    "PING": "api/v2/ping/",
    "USER_INFO": "api/v2/connected-user/",
    "BILL_INIT": "api/v2/payments/bill/init/",
    "BILL_VERIFY": "api/v2/payments/bill/verify/",
    "CASHIN": "api/v2/payments/cash-in/",
    # "BANKS": "api/v2/bank/all",
    "BANKS": "api/v2/payments/bank/",
    "BANKS_ALL": "api/v2/payments/bank/%s/",
    "LOOKUP": "api/v2/bank/%s/account/lookup/",
}


class MerchantClient(object):
    no_auth_response = {
        "success": False,
        "response_code": "401",
        "response_message": "The client is not authenticated",
        "response_data": {"authentication": "The client is not authenticated"},
    }

    def __init__(
        self, client_id, client_secret, pin_code, state=None, prod=False, ihela_url=None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_object = None
        self.redirect_uri = None
        self.state = state
        self.prod_env = prod
        self.pin_code = pin_code

        self.ihela_base_url = iHela_BASE_URL

        if ihela_url:
            self.ihela_base_url = ihela_url

        elif self.prod_env is True:
            self.ihela_base_url = iHela_BASE_URL

        elif self.prod_env is False:
            self.ihela_base_url = iHela_BASE_TEST_URL

        else:
            self.ihela_base_url = iHela_BASE_TEST_URL

        self.authenticate()

    def get_response(self, resp):
        try:
            resp_json = dict(resp.json())
            resp_json["response_status"] = resp.status_code
            logger.debug(resp_json)
            return resp_json
        except (json.decoder.JSONDecodeError, simplejson.errors.JSONDecodeError):
            logger.error("IHELA_CLIENT_ERROR : %s" % resp.text)
            return {
                "errors": {"request": "An error occured during request"},
                "bill": {},
            }

    def get_url(self, url):
        return f"{self.ihela_base_url}{url}"

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
            # Don't make auth_data logger on production
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

    def ping(self):
        """
        This returns the connection availability with iHela servers
        """
        ping_info_ = requests.get(self.get_url(iHela_ENDPOINTS["PING"]))
        ping_info = self.get_response(ping_info_)

        return ping_info

    def customer_lookup(self, bank_slug, customer_id):
        """
        This returns a customer info in the given bank
        """
        url = iHela_ENDPOINTS["LOOKUP"] % bank_slug
        customer_info_ = requests.get(
            self.get_url(url),
            params={"account_number": customer_id},
            headers=self.get_auth_headers(),
        )
        customer_info = self.get_response(customer_info_)

        return customer_info

    def init_bill(
        self,
        amount,
        user,
        description,
        reference,
        bank=None,
        bank_client_id=None,
        redirect_uri=None,
    ):
        if self.is_authenticated():
            if bank and not bank_client_id:
                bank_client_id = user
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
            return self.no_auth_response

    def verify_bill(self, code, reference):
        bill_data = {"code": code, "reference": reference}
        url = iHela_ENDPOINTS["BILL_VERIFY"]
        bill_ = requests.post(
            self.get_url(url), data=bill_data, headers=self.get_auth_headers()
        )
        bill_verified = self.get_response(bill_)

        return bill_verified

    def cashin_client(
        self,
        bank_slug,
        account,
        account_holder,
        amount,
        merchant_reference,
        description,
    ):
        if self.is_authenticated():
            cashin_data = {
                "credit_bank": bank_slug,
                "credit_account": account,
                "credit_account_holder": account_holder,
                "amount": amount,
                "merchant_reference": merchant_reference,
                "description": description,
                "pin_code": self.pin_code,
            }
            url = iHela_ENDPOINTS["CASHIN"]
            cashin_ = requests.post(
                self.get_url(url), data=cashin_data, headers=self.get_auth_headers()
            )
            cashin = self.get_response(cashin_)

            return cashin
        else:
            return self.no_auth_response

    def get_bank_list(self, list_type=None):
        if not list_type:
            list_type = "cashin"
        if self.is_authenticated():
            url = iHela_ENDPOINTS["BANKS_ALL"] % list_type
            banks_ = requests.get(self.get_url(url), headers=self.get_auth_headers())
            banks = self.get_response(banks_)

            return banks
        else:
            return self.no_auth_response


if __name__ == "__main__":
    client_id = "4sS7OWlf8pqm04j1ZDtvUrEVSZjlLwtfGUMs2XWZ"
    client_id = "12CMmsS2e3aqONxYHCSpHaG3p7VWls9vtczbNk1b"
    # client_id = "KziHxNoydAhWV2uVSfimZf7ApMY1tdjW9vYXfGwk"
    client_secret = "HN7osYwSJuEOO4MEth6iNlBS8oHm7LBhC8fejkZkqDJUrvVQodKtO55bMr845kmplSlfK3nxFcEk2ryiXzs1UW1YfVP5Ed6Yw0RR6QmnwsQ7iNJfzTgeehZ2XM9mmhC3"
    client_secret = "duwbLBiKPoJTytFnMcAbP8QxmaAJPboNQHslRpqgCsSplNo5Es4tBFDJl2Iae0WAErpP4QcQ0iUGpxkoFdFXnOeGDMvtX5JLVyrlvRE6DfScBagKExHdmugWwDstFHgP"
    # client_secret = "LjATwjOk70mGVdkyGZNxRih0FLe4lfF2UEgHAGAF7ovK38jQQ9dBdd1SSmWoXZl44wee0bFamQQclq1sQFUBL6XBsGqjRV8DR8isa2GEVNNMroLWiB1K5ZZf3H9UoCyt"
    cl = MerchantClient(
        client_id,
        client_secret,
        pin_code="1234",
        ihela_url="http://10.30.0.7/",
    )
    # )  # , ihela_url="http://127.0.0.1:8080/")
    print("\nPING IHELA : ", cl.ihela_base_url)
    ping = cl.ping()
    print("PING DATA : ", ping)

    # bill = cl.init_bill(
    #     2000,
    #     # "76077736",
    #     "pierreclaverkoko@gmail.com",
    #     "My description",
    #     str(secrets.token_hex(10)),
    #     # bank="MOB-0003"
    # )
    # print(bill)

    # if bill["bill"].get("merchant_reference"):
    #     bill_verif = cl.verify_bill(
    #         bill["bill"]["merchant_reference"], bill["bill"]["code"]
    #     )

    #     print("\nBILL VERIFY : ", bill_verif)

    banks = cl.get_bank_list()

    print("\nBANKS LIST : ", banks)

    client = cl.customer_lookup("MF1-0001", "000016-01")

    print("\nCUSTOMER LOOKUP : ", client)

    cashin = cl.cashin_client(
        "MF1-0001",
        "000016-01",
        "Pierre Claver Koko",
        20000,
        str(secrets.token_hex(10)),
        "Cashin description",
    )

    print("\nCASHIN TO CLIENT : ", cashin)
