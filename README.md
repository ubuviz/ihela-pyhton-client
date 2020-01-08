# iHela Client

This repository provides a Python client for iHela platform.

## Get started

1. Install the package with `pip install ihela-python-client`
2. import the package for using the provided functions to communicate with the iHela API
```python
from ihela_client.client import Client 

CLIENT_ID = "<Your Client ID>"
CLIENT_SECRET = "<Your Client Secret>"
TEST_ENV = True

cl = Client(CLIENT_ID, CLIENT_SECRET, test=TEST_ENV)
redirect_uri = "https://yourapp.com/uri/to/redirect/to/"

auth_url = cl.get_authorization_url(redirect_uri)
```
The `redirect_uri` must be registered with the client created by iHela both for test and production.
3. Redirect to the returned `auth_url`: This will allow the user to authorize your application to access the iHela website banking operations and will redirect to your `redirect_uri` with an authorization code passed as GET method parameter.
4. The `redirect_uri` must handle the received authorization code and pass to the authenticate url like this :  
``` python
# Get the authorization code
# For example in django : authorization_code_received = request.GET.get("code")

# Then call the authenticate method
cl.authenticate(authorization_code=auth_code_received)

# To verifiy that the user is well authenticated :
cl.is_authenticated() # Must return True if the authentication went well
```
