# This class was generated on Mon, 02 Jul 2018 17:09:03 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# orders_authorize_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class OrdersAuthorizeRequest:
    """
    Authorizes payment for an order. The response shows authorization details.
    """

    def __init__(self, order_id):
        self.verb = "POST"
        self.path = "/v2/checkout/orders/{order_id}/authorize?".replace("{order_id}", quote(str(order_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def pay_pal_client_metadata_id(self, pay_pal_client_metadata_id):
        self.headers["PayPal-Client-Metadata-Id"] = str(pay_pal_client_metadata_id)

    def pay_pal_request_id(self, pay_pal_request_id):
        self.headers["PayPal-Request-Id"] = str(pay_pal_request_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, order_action_request):
        self.body = order_action_request
        return self
