# This class was generated on Tue, 10 Jul 2018 10:40:35 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# authorizations_reauthorize_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# @data 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
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class AuthorizationsReauthorizeRequest:
    ***REMOVED***
    Reauthorizes an authorized PayPal account payment, by ID. To ensure that funds are still available, reauthorize an authorized payment after its initial three-day honor period expires.<br/><br/>After the three-day honor period expires,
    you can reauthorize an authorized payment only once from days four to 29. If 30 days have passed since the date of
    the authorized payment, you must create an authorized payment instead.<br/><br/>A
    reauthorized payment itself has a new three-day honor period. You can reauthorize an authorized payment once
    for up to 115% of the original authorized amount and not to exceed an increase of $75 USD.<br/><br/>Supports
    the <code>amount</code> request parameter only.
    ***REMOVED***
    def __init__(self, authorization_id):
        self.verb = "POST"
        self.path = "/v2/payments/authorizations/{authorization_id}/reauthorize?".replace("{authorization_id}", quote(str(authorization_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def pay_pal_request_id(self, pay_pal_request_id):
        self.headers["PayPal-Request-Id"] = str(pay_pal_request_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, reauthorize_request):
        self.body = reauthorize_request
        return self
