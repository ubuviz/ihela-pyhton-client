iHela Client
============

This repository provides a Python client for iHela platform.

Get started
-----------


1. Install the package with ``pip install ihela-python-client``
2. import the package for using the provided functions to communicate with the iHela API
The ``redirect_uri`` must be registered with the client created by iHela both for test and production.

3. Redirect to the returned ``auth_url``: This will allow the user to authorize your application to access the iHela website banking operations and will redirect to your ``redirect_uri`` with an authorization code passed as GET method parameter.
4. The ``redirect_uri`` must handle the received authorization code and pass to the authenticate url like this : 

5. After authentication, 
