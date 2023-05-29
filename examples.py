try:
    import secrets
except ImportError:  # Python < 3.6
    import random as secrets

from ihela_client.merchant_client import MerchantClient

client_id = "4sS7OWlf8pqm04j1ZDtvUrEVSZjlLwtfGUMs2XWZ"
client_id = "12CMmsS2e3aqONxYHCSpHaG3p7VWls9vtczbNk1b"
# client_id = "KziHxNoydAhWV2uVSfimZf7ApMY1tdjW9vYXfGwk"
client_secret = "HN7osYwSJuEOO4MEth6iNlBS8oHm7LBhC8fejkZkqDJUrvVQodKtO55bMr845kmplSlfK3nxFcEk2ryiXzs1UW1YfVP5Ed6Yw0RR6QmnwsQ7iNJfzTgeehZ2XM9mmhC3"  # noqa
client_secret = "duwbLBiKPoJTytFnMcAbP8QxmaAJPboNQHslRpqgCsSplNo5Es4tBFDJl2Iae0WAErpP4QcQ0iUGpxkoFdFXnOeGDMvtX5JLVyrlvRE6DfScBagKExHdmugWwDstFHgP"  # noqa
# client_secret = "LjATwjOk70mGVdkyGZNxRih0FLe4lfF2UEgHAGAF7ovK38jQQ9dBdd1SSmWoXZl44wee0bFamQQclq1sQFUBL6XBsGqjRV8DR8isa2GEVNNMroLWiB1K5ZZf3H9UoCyt" # noqa
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

cashin_reference = str(secrets.token_hex(10))
cashin = cl.cashin_client(
    "MF1-0001",
    "000016-01",
    "Pierre Claver Koko",
    20000,
    cashin_reference,
    "Cashin description",
)
print("\nCASHIN TO CLIENT : ", cashin_reference, " ::: ", cashin)

cashin_resp_data = cashin.get("response_data", {})
ihela_reference = cashin_resp_data.get("reference") if cashin_resp_data else None
operations_status = cl.operations_status(
    external_reference="cashin_reference",
    ihela_reference=ihela_reference,
)
print(
    "\nOPERATION STATUS : ",
    cashin_reference,
    " >< ",
    ihela_reference,
    " ::: ",
    operations_status,
)
