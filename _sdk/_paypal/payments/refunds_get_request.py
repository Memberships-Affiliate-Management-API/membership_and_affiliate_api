# This class was generated on Tue, 10 Jul 2018 10:40:35 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# refunds_get_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class RefundsGetRequest:
    ***REMOVED***
    Shows details for a refund, by ID.
    ***REMOVED***
    def __init__(self, refund_id):
        self.verb = "GET"
        self.path = "/v2/payments/refunds/{refund_id}?".replace("{refund_id}", quote(str(refund_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None


