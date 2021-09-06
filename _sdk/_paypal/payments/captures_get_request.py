# This class was generated on Tue, 10 Jul 2018 10:40:35 PDT by version 0.1.0-dev+0ee05a-dirty of Braintree SDK Generator
# captures_get_request.py
# @version 0.1.0-dev+0ee05a-dirty
# @type request
# DO NOT EDIT
import paypalhttp
from urllib.parse import quote  # Python 3+


# noinspection PyDictCreation
class CapturesGetRequest:
    """
    Shows details for a captured payment, by ID.
    """
    def __init__(self, capture_id):
        self.verb = "GET"
        self.path = "/v2/payments/captures/{capture_id}?".replace("{capture_id}", quote(str(capture_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None


