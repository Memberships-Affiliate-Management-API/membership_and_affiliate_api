# This class was generated on Tue, 10 Jul 2018 10:40:35 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# authorizations_void_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class AuthorizationsVoidRequest:
    ***REMOVED***
    Voids, or cancels, an authorized payment, by ID. You cannot void an authorized payment that has been fully captured.
    ***REMOVED***
    def __init__(self, authorization_id):
        self.verb = "POST"
        self.path = "/v2/payments/authorizations/{authorization_id}/void?".replace("{authorization_id}", quote(str(authorization_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None


