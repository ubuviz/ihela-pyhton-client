# iHela Client

This is the repository for a Python client for consuming the iHela Crédit Union API for financial services in Burundi. The API gateway can be found on https://testgate.ihela.online/

## Get started

### Installation

Install the package with `pip install ihela-python-client`

### Get a client instance

import the package for using the provided functions to communicate with the iHela API
```python
from ihela_client import MerchantClient 

CLIENT_ID = "<Your Client ID>"
CLIENT_SECRET = "<Your Client Secret>"
PROD_ENV = False

cl = MerchantClient(CLIENT_ID, CLIENT_SECRET, prod=PROD_ENV)
redirect_uri = "https://yourapp.com/uri/to/redirect/to/"

```
The `redirect_uri` must be registered with the client created by iHela both for test and production. This is not mandatory.

### Initialize Bill

Call bills functions as shown below
```python
# cl.init_bill(AMOUNT, USER_EMAIL, TRANSACTION_DESCRIPTION, MERCHANT_REFERENCE, redirect_uri=URL)
bill = cl.init_bill(2000, "clientmail@gmail.com", "My description", "unique_reference", redirect_uri=redirect_uri)
```
Here is a response sample. You must have a copy of the "code" and the "confirmation_uri" and other data you judge important. The confirmation_uri provides a direct url to the bill in iHela. You can directly redirect the user to.
```json
{
	"bill": {
	    "merchant": {
	        "title": "Global Test Merchant",
	        "merchant": {
	            "id": 6,
	            "title": "Global Test Merchant",
	            "merchant_type": {"label": "Biller", "value": "B", "css": null},
	            "merchant_slug": "global-test-merchant",
	            "merchant_logo": null,
	            "merchant_code": 16
	        },
	        "user": {
	            "username": "merchant-username",
	            "email": "merchantmail@gmail.com",
	            "ihela_code": "1",
	            "bio": "Merchant bio",
	            "image": "https://testgate.ihela.online/vwmedia/users/profiles/d7c-4c38-ae24-284f1b554b92.png",
	            "following": false
	        },
	    },
	    "initiated_by": {
	        "username": "client-username",
	        "email": "clientmail@gmail.com",
	        "ihela_code": "2",
	        "bio": "Client bio",
	        "image": "https://testgate.ihela.online/vwmedia/users/profiles/d7c257a1b554b92.png",
	        "following": false
	    },
	    "paid_by": null,
	    "amount": "2000.00",
	    "currency": 108,
	    "currency_info": {
	        "iso_code": 108,
	        "iso_alpha_code": "BIF",
	        "title": "BURUNDIAN FRANC",
	        "abbreviation": "BIF",
	        "operation_min_amount": "1.00"
	    },
	    "description": "Global Test Merchant (1) My description 58646cc904c471d6413e",
	    "merchant_reference": "58646cc904c471d6413e",
	    "status": {"label": "Initiated", "value": "I", "css": "tag is-info"},
	    "expired": false,
	    "code": "BILL-20200813-B8GUIUDIN0",
	    "redirect_uri": null,
	    "confirmation_uri": "https://mytest.ihela.online/u/operations/bill/confirm/BILL-20200813-B8GUIUDIN0",
	    "payment_reference": null,
	    "created_at": "2020-08-13T10:24:58.014322Z"
	},
	"response_status": 200
}
```

### Verify a bill

You can then verify after if the user has paid the bill in iHela. (NB: He must go to iHela and pay). You can provide a background task or a reload button in your interface for checking.
``` python
cl.verify_bill(bill["bill"]["merchant_reference"], bill["bill"]["code"])
```
Here is a response sample. Bill can be **Pending**, **Paid** or **Expired**. If bill is paid, "bank_reference" will return the transaction reference in the bank.
```json
{
    "bill": {
        "bank_reference": null,
        "reference": "BILL-20200813-B8GUIUDIN0",
        "code": "58646cc904c471d6413e",
        "status": "Pending"
    },
    "response_status": 200
}
```

### Cashin client account

If your client has to be refunded or gratified directly in this account in our system, use the **cashin** operation.
```python
# Get banks using the function below and provide a select widget to the user to get a bank slug

```
The bank list response gives the bank information that can help you provide a complete widget on your side (name, type, different codes, logo and icon, account_masked_text for using a formatted widget ...)
```json

{
    "banks": [
        {
            "slug": "MF1-0001",
            "name": "iHela Credit Union",
            "swift_code": null,
            "bank_code": 1,
            "bank_type": "MF1",
            "can_create_account_online": true,
            "is_active": true,
            "company": {
                "name": "iHela",
                "nickname": null,
                "slug": "ihela",
                "about": "",
                "logo": "https://testgate.ihela.online/vwmedia/addressbook/companies/ihelalogo.jpg",
                "logo_icon": "https://testgate.ihela.online/vwmedia/addressbook/companies/icon/ihela_favicon_red.png",
            },
            "account_masked_text": "000000-00",
        },
        {
            "slug": "BNQ-0002",
            "name": "Mutec",
            "swift_code": null,
            "bank_code": 2,
            "bank_type": "BNQ",
            "can_create_account_online": false,
            "is_active": true,
            "company": {
                "name": "Mutec",
                "nickname": null,
                "slug": "mutec",
                "about": "",
                "logo": "https://testgate.ihela.online/vwmedia/addressbook/companies/logo-mutec-best.png",
                "logo_icon": "https://testgate.ihela.online/vwmedia/addressbook/companies/icon/logo-mutec-best.png",
            },
            "account_masked_text": null,
        },
    ],
    "banksCount": 2,
    "response_status": 200,
}

```
Having the bank will help getting the slug for cashin.

```python
# cashin = cl.cashin_client(BANK_SLUG, ACCOUNT_NUMBER, AMOUNT, MERCHANT_REFERENCE, TRANSACTION_DESCRIPTION)
cashin = cl.cashin_client("MF1-0001", "000016-01", 20000, "REF3223", "Cashin description")
```
Here is an sample example

```json
{
    "bank_slug": "MF1-0001",
    "account": "000016-01",
    "amount": "20000.00",
    "description": "Cashin description",
    "merchant_reference": "REF3223",
    "error": false,
    "error_message": "Success",
    "reference": "CPT-5/01-199",
    "response_status": 200,
}
```
