
import paypalhttp

from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class OrdersGetRequest:
    ***REMOVED***
    Shows details for an order, by ID.
    ***REMOVED***
    def __init__(self, order_id):
        self.verb = "GET"
        self.path = "/v2/checkout/orders/{order_id}?".replace("{order_id}", quote(str(order_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None


