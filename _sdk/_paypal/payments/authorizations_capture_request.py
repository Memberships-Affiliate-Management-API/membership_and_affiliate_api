# This class was generated on Tue, 10 Jul 2018 10:40:35 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# authorizations_capture_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# @data
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


class AuthorizationsCaptureRequest:
    ***REMOVED***
    Captures an authorized payment, by ID.
    ***REMOVED***

    def __init__(self, authorization_id):
        self.verb = "POST"
        self.path = "/v2/payments/authorizations/{authorization_id}/capture?".replace("{authorization_id}",
                                                                                      quote(str(authorization_id)))
        self.headers = {"Content-Type": "application/json"}
        self.body = None

    def pay_pal_request_id(self, pay_pal_request_id):
        self.headers["PayPal-Request-Id"] = str(pay_pal_request_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, capture):
        self.body = capture
        return self
