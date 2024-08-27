# iHela Client

This is the repository for a Python client for consuming the iHela Crédit Union API for financial services in Burundi. The API gateway can be found on https://api.ihela.bi/testenv/

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
    "response_code": "00",
    "response_data": {
        "objects": [
            {
                "id": 1,
                "slug": "MF1-0001",
                "name": "IHELÁ CREDIT UNION",
                "swift_code": null,
                "bank_code": 1,
                "bank_type": "MF1",
                "can_create_account_online": true,
                "is_active": true,
                "company": {
                    "name": "IHELÁ CREDIT UNION",
                    "fullname": "IHELÁ CREDIT UNION",
                    "nickname": "ICU",
                    "slug": "0000000002",
                    "image": "https://testcbsdbs.ihela.bi/media/clients/corporate/2_ihela.png",
                    "about": "IHELÁ CREDIT UNION",
                    "logo": "https://testcbsdbs.ihela.bi/media/clients/corporate/2_ihela.png",
                    "logo_icon": "https://testcbsdbs.ihela.bi/media/clients/corporate/2_ihela_logo_red.png"
                },
                "limits_config": null,
                "account_masked_text": null,
                "is_default": true,
                "api_values": {
                    "has_lookup": true,
                    "has_cashin": true,
                    "has_cashout": true,
                    "has_integrated_too": false,
                    "additional_api_list": [
                        "agent_agent_transfer",
                        "agent_lookup"
                    ]
                }
            }
        ],
        "count": 7
    },
    "response_message": "Done",
    "success": true,
    "response_status": 200
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
{
    "response_code": "00",
    "response_data": {
        "account_number": "30001-01-00-0000000001-01-95",
        "name": "Bizimana Jean Claude"
    },
    "response_message": "Success",
    "success": true
}
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
    "response_code": "00",
    "response_data": {
        "code": "CODE-20230321-9E29QH1",
        "reference": null
    },
    "response_message": "Payment bill successfully created. The client has to validate it to complete the payment. Code : CODE-20230321-9E29QH1",
    "success": true
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
  "response_code": "00",
  "response_data": {
    "bill_code": "CODE-20230321-JQ4H26F",
    "merchant_reference": "752000",
    "payment_reference": null,
    "status": "Initial"
  },
  "response_message": "Done",
  "success": true
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
    "response_code": "00",
    "response_data": {
        "reference": "29032360510975",
        "bank_reference": "123456",
        "pending_id": 975,
        "date": "2023-03-29T09:16:24.396951Z",
        "is_partial": false
    },
    "response_message": "Transaction successfully done. Reference: 29032360510975 >> mTSF.3000100-756.3000101-2108",
    "success": true
}
```
