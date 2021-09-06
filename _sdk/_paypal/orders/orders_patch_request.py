import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class OrdersPatchRequest:
    """
    Updates an order. You can update an order with `CREATED` or `APPROVED` status. You cannot update an order with `COMPLETED` status. The following attributes and objects are patchable:<ul><li><code>intent</code>. Supported operation is <code>replace</code>.</li><li><code>purchase_units</code>. Supported operations are <code>add</code> and <code>replace</code>.</li><li><code>purchase_units[].custom_id</code>. Supported operations are <code>add</code> and <code>replace</code> and <code>remove</code>.</li><li><code>purchase_units[].description</code>. Supported operations are <code>add</code> and <code>replace</code> and <code>remove</code>.</li><li><code>purchase_units[].payee.email</code>. Supported operations are <code>add</code> and <code>replace</code>.</li><li><code>purchase_units[].shipping_address</code>. Supported operations are <code>add</code> and <code>replace</code> and <code>remove</code>.</li><li><code>purchase_units[].soft_descriptor</code>. Supported operations are <code>add</code> and <code>replace</code> and <code>remove</code>.</li><li><code>purchase_units[].amount</code>. Supported operation is <code>replace</code>.</li></ul>
    """
    def __init__(self, order_id):
        self.verb = "PATCH"
        self.path = "/v2/checkout/orders/{order_id}?".replace("{order_id}", quote(str(order_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

    def request_body(self, patch_request):
        self.body = patch_request
        return self
