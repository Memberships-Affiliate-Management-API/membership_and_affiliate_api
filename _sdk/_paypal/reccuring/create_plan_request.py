import paypalhttp
from urllib.parse import quote  # Python 3+
#
# curl -v -X POST https://api-m.sandbox.paypal.com/v1/catalogs/products \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer <Access-Token>" \
#   -H "PayPal-Request-Id: <merchant-generated-ID>" \ // Optional and if passed, helps identify idempotent requests
# -d '{
#   "name": "Video Streaming Service",
#   "description": "Video streaming service",
#   "type": "SERVICE",
#   "category": "SOFTWARE",
#   "image_url": "https://example.com/streaming.jpg",
#   "home_url": "https://example.com/home"
# }'


class PlansCreatePlan:

    def __init__(self):
        self.verb = "POST"
        self.path = "/v1/billing/plans"
        self.headers = {"Content-Type": "application/json"}
        self.body = None

    def pay_pal_client_metadata_id(self, pay_pal_client_metadata_id):
        # merchant generated id
        self.headers["PayPal-Client-Metadata-Id"] = str(pay_pal_client_metadata_id)

    def pay_pal_request_id(self, pay_pal_request_id):
        self.headers["PayPal-Request-Id"] = str(pay_pal_request_id)

    def prefer(self, prefer):
        self.headers["Prefer"] = str(prefer)

    def request_body(self, service_action_request):
        self.body = service_action_request
        return self
