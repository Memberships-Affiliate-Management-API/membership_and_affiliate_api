

import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class OrdersCreateRequest:
    ***REMOVED***
    Creates an order.
    ***REMOVED***
    def __init__(self):
        self.verb = "POST"
        self.path = "/v2/checkout/orders?"
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def pay_pal_partner_attribution_id(self, pay_pal_partner_attribution_id):
        self.headers["PayPal-Partner-Attribution-Id"] = str(pay_pal_partner_attribution_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, order):
        self.body = order
        return self
