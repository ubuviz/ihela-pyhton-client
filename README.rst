iHela Client
============

This repository provides a Python client for iHela platform.

Get started
-----------


#. Install the package with ``pip install ihela-python-client``
#. import the package for using the provided functions to communicate with the iHela API
::

   from ihela_client.client import Client 

   CLIENT_ID = "<Your Client ID>"
   CLIENT_SECRET = "<Your Client Secret>"
   TEST_ENV = True

   cl = Client(CLIENT_ID, CLIENT_SECRET, test=TEST_ENV)
   redirect_uri = "https://yourapp.com/uri/to/redirect/to/"

   auth_url = cl.get_authorization_url(redirect_uri)

The `redirect_uri` must be registered with the client to be used.
#. Redirect to the returned `auth_url` : This will allow the user to login in the iHela website and allow your application with an authorization code. After login, the user will be redirect to the given `redirect_uri`.
#. The `redirect_uri` must handle the received authorization code and pass to the authenticate url : 
::
   cl.authenticate(authorization_code=auth_code_received)

   # To verifiy that the user is well authenticated :
   cl.is_authenticated() # Must return True if the authentication went well
