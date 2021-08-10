import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class OrdersValidateRequest:
    ***REMOVED***
    Validates a payment method and checks it for contingencies.
    ***REMOVED***
    def __init__(self, order_id):
        self.verb = "POST"
        self.path = "/v2/checkout/orders/{order_id}/validate-payment-method?".replace("{order_id}", quote(str(order_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def pay_pal_client_metadata_id(self, pay_pal_client_metadata_id):
        self.headers["PayPal-Client-Metadata-Id"] = str(pay_pal_client_metadata_id)

    def request_body(self, order_action_request):
        self.body = order_action_request
        return self
