import requests

import settings as client_settings


class Client(object):
    def __init__(self, client_id, client_secret, ihela_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_object = None

        self.ihela_base_url = client_settings.iHela_BASE_URL
        if ihela_url:
            self.ihela_base_url = ihela_url

    def get_url(self, url):
        return self.ihela_base_url + str(url)

    def authenticate(self, username, password):
        url = client_settings.iHela_AUTH_URL
        auth_ = requests.post(
            self.get_url(url),
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": username,
                "password": password,
            },
        )
        try:
            self.auth_token_object = auth_.json()
        except ImportError:  # TODO: Change the Exception catch here
            self.auth_token_object = None

        return auth_

    def is_authenticated(self):
        return self.auth_token_object is not None


if __name__ == "__main__":
    client_id = "jHHXDnl7zZUofkbbIznC8iUrez8iATeH8TihQDgh"
    client_secret = "n2dLFUe12XnpS9bzc7EYS6CfKkSQP1LuCVWY65YECJIkXoXc3cmycUrMyybqfSdNQeItVOyLmCYAh4b9cdd76T0nSn1RnP1XktcJPHWRjwBptaYaIzG5oKXi6TTaodQe"

    cl = Client(client_id, client_secret, ihela_url="http://127.0.0.1:8080/")

    cl.authenticate(username="pierreclaverkoko@gmail.com", password="pass123456")

    print("Authenticated : ", cl.is_authenticated())
