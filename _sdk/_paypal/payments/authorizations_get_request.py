# This class was generated on Tue, 10 Jul 2018 10:40:35 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# authorizations_get_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


class AuthorizationsGetRequest:
    ***REMOVED***
    Shows details for an authorized payment, by ID.
    ***REMOVED***

    def __init__(self, authorization_id):
        self.verb = "GET"
        self.path = "/v2/payments/authorizations/{authorization_id}?".replace("{authorization_id}",
                                                                              quote(str(authorization_id)))
        self.headers = {"Content-Type": "application/json"}
        self.body = None
