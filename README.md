# iHela Client

This repository provides a Python client for iHela platform.

## Get started

1. Install the package with `pip install ihela-python-client`
2. import the package for using the provided functions to communicate with the iHela API
```python
from ihela_client import Client 

CLIENT_ID = "<Your Client ID>"
CLIENT_SECRET = "<Your Client Secret>"
TEST_ENV = True

cl = Client(CLIENT_ID, CLIENT_SECRET, test=TEST_ENV)

cl.authenticate(username="pierreclaverkoko@gmail.com", password="pass123456")

# To verifiy that the user is well authenticated :
cl.is_authenticated() # Must return True if the authentication went well
```