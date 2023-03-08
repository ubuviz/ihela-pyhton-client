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
Set `PROD_ENV = True` for production, otherwise set it to `PROD_ENV = False`
The `redirect_uri` must be registered with the client created by iHela both for test and production. This is not mandatory.

### Bank list

This returns the banks list for getting their slugs for the requests.

```python
# cl.init_bill(AMOUNT, USER_EMAIL, TRANSACTION_DESCRIPTION, MERCHANT_REFERENCE, BANK, BANK_CLIENT_ID,redirect_uri=URL)
banks = cl.get_bank_list()
```
The bank list response gives the bank information that can help you provide a complete widget on your side (name, type, different codes, logo and icon, ...)

```python
{
    "banks": [
        {
            "slug": "MF1-0001",
            "name": "iHela Credit Union",
            "swift_code": None,
            "bank_code": 1,
            "bank_type": "MF1",
            "can_create_account_online": True,
            "is_active": True,
            "company": {
                "name": "Ihelá Credit Union",
                "fullname": "Ihelá Credit Union",
                "nickname": "ICU",
                "slug": "ihela-credit-union",
                "image": "https://testgate.ihela.online/vwmedia/addressbook/companies/ihelalogo_DCklq5H.jpg",
                "about": "Ihelá Credit Union",
                "logo": "https://testgate.ihela.online/vwmedia/addressbook/companies/ihelalogo_DCklq5H.jpg",
                "logo_icon": "https://testgate.ihela.online/vwmedia/addressbook/companies/icon/ihelacreditunionfondblanc.png",
            },
            "limits_config": None,
            "account_masked_text": "000000-00",
            "ihela_account_inside": None,
        },
        {
            "slug": "MOB-0003",
            "name": "EcoCash",
            "swift_code": None,
            "bank_code": 3,
            "bank_type": "MOB",
            "can_create_account_online": False,
            "is_active": True,
            "company": {
                "name": "EcoCash",
                "fullname": "EcoCash",
                "nickname": None,
                "slug": "ecocash",
                "image": "https://testgate.ihela.online/vwmedia/addressbook/companies/logoEcoCash.gif",
                "about": "",
                "logo": "https://testgate.ihela.online/vwmedia/addressbook/companies/logoEcoCash.gif",
                "logo_icon": "https://testgate.ihela.online/vwmedia/addressbook/companies/icon/logoEcoCash_LfUl0cA.gif",
            },
            "limits_config": None,
            "account_masked_text": "00000000",
            "ihela_account_inside": None,
        },
        {
            "slug": "MOB-0006",
            "name": "PesaFlash",
            "swift_code": None,
            "bank_code": 6,
            "bank_type": "MOB",
            "can_create_account_online": False,
            "is_active": True,
            "company": {
                "name": "Pesaflashjklfs",
                "fullname": "Pesaflashjklfs",
                "nickname": "-",
                "slug": "pesaflashjklfs",
                "image": "https://testgate.ihela.online/vwmedia/addressbook/companies/FINBANK_LANDSCAPE_MxkUXas.png",
                "about": "Pesaflash",
                "logo": "https://testgate.ihela.online/vwmedia/addressbook/companies/FINBANK_LANDSCAPE_MxkUXas.png",
                "logo_icon": "https://testgate.ihela.online/vwmedia/addressbook/companies/icon/FINBANK_LANDSCAPE_A0DFqu8.png",
            },
            "limits_config": {
                "in_minimum": "10000.00",
                "in_maximum": "50000000.00",
                "out_minimum": "10000.00",
                "out_maximum": "50000000.00",
            },
            "account_masked_text": None,
            "ihela_account_inside": None,
        },
    ],
    "count": 3,
    "response_status": 200,
}
```

### Customer Lookup

We will make a customer lookup for having the account number to use in the cashin function.

```python
# cashin = cl.cashin_client(BANK_SLUG, ACCOUNT_NUMBER, AMOUNT, MERCHANT_REFERENCE, TRANSACTION_DESCRIPTION)
customer_lookup = cl.customer_lookup(bank_slug=selected_bank["slug"], customer_id="76000111")
```

And you get the acccount_number :

```python
{'account_number': '000001-01', 'name': 'Bigirimana Fabrice', 'response_status': 200}
```
The name can be prompted so that the user can confirm there is no error.


### Initialize Bill

Call bills functions as shown below. The function accepts the user email, user phone number or user ihela id
```python
# cl.init_bill(AMOUNT, USER_EMAIL, TRANSACTION_DESCRIPTION, MERCHANT_REFERENCE, BANK, BANK_CLIENT_ID,redirect_uri=URL)
bill = cl.init_bill(2000, "clientmail@gmail.com", "My description", "unique_reference", redirect_uri=redirect_uri)
```
BANK and BANK_CLIENT_ID are optional, They are used when the transaction is made from a third party Bank or Institution.

```python
bank_slug = selected_bank["slug"]

# cl.init_bill(AMOUNT, USER_EMAIL, TRANSACTION_DESCRIPTION, MERCHANT_REFERENCE, BANK, BANK_CLIENT_ID,redirect_uri=URL)
bill = cl.init_bill(2000, "76000111", "My description", "unique_reference", bank=bank_slug, bank_client_id="76000111", redirect_uri=redirect_uri)
```

Here is a response sample. You must have a copy of the "code" and the "confirmation_uri" and other data you judge important. The confirmation_uri provides a direct url to the bill in iHela. You can directly redirect the user to.

```python
{
	"bill": {
	    "merchant": {
	        "title": "Global Test Merchant",
	    },
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
	    "expired": False,
	    "code": "BILL-20200813-B8GUIUDIN0",
	    "redirect_uri": None,
	    "confirmation_uri": "https://mytest.ihela.online/u/operations/bill/confirm/BILL-20200813-B8GUIUDIN0",
	    "payment_reference": None,
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
```python
{
    "bill": {
        "bank_reference": None,
        "reference": "BILL-20200813-B8GUIUDIN0",
        "code": "58646cc904c471d6413e",
        "status": "Pending"
    },
    "response_status": 200
}
```

### Cashin client account

If your client has to be refunded or gratified directly in this account in our system, use the **cashin** operation.
The variable `customer_lookup` is from the client lookup function here above.

```python
# cashin = cl.cashin_client(BANK_SLUG, ACCOUNT_NUMBER, AMOUNT, MERCHANT_REFERENCE, TRANSACTION_DESCRIPTION)
cashin = cl.cashin_client("MF1-0001", customer_lookup["account_number"], 20000, "REF3223", "Cashin description")
```
Here is a response sample

```json
{
    "bank_slug": "MF1-0001",
    "account": "000001-01",
    "amount": "20000.00",
    "description": "Cashin description",
    "merchant_reference": "REF3223",
    "error": false,
    "error_message": "Success",
    "reference": "CPT-5/01-199",
    "response_status": 200,
}
```
