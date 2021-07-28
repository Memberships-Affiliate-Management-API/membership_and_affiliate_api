import typing
from flask import url_for, json
from _sdk._paypal.paypal_client import PayPalClient
from _sdk._paypal.orders import OrdersCreateRequest, OrdersAuthorizeRequest
from _sdk._paypal.payments import AuthorizationsCaptureRequest
from _sdk._paypal.reccuring import PlansCreateServiceProduct
from database.mixins import AmountMixin


class PayPalOrders(PayPalClient):
    ***REMOVED***Setting up the complete JSON request body for creating the Order. The Intent in the
        request body should be set as "AUTHORIZE" for capture intent flow.***REMOVED***

    ***REMOVED***Setting up the minimum required JSON request body for creating the Order. The Intent in the
        request body should be set as "AUTHORIZE" for capture intent flow.***REMOVED***
    order_response = None
    authorize_response = None
    capture_response = None

    def __init__(self, app, reference_id: str, description: str, custom_id: str, soft_descriptor: str, payment_amount: AmountMixin):
        super(PayPalOrders, self).__init__(app=app)
        self.reference_id: str = reference_id
        self.description: str = description
        # NOTE: custom_id should always equal organization_id
        self.custom_id: str = custom_id
        self.soft_descriptor: str = soft_descriptor
        self.payment_amount: AmountMixin = payment_amount
        self.order_id: typing.Union[str, None] = None
        self.authorization_id: typing.Union[str, None] = None

    def build_order_request_body(self) -> dict:
        ***REMOVED***Method to create body with AUTHORIZE intent***REMOVED***
        return {
            "intent": "AUTHORIZE",
            "application_context": {
                "return_url": "{}".format(url_for('paypal_ipn.deposit_successfull_ipn', path=''.format(self.custom_id))),
                "cancel_url": "".format(url_for('paypal_ipn.deposit_cancelled_ipn', path=''.format(self.custom_id))),
                "brand_name": "Memberships & Affiliates Management API",
                "landing_page": "BILLING",
                "user_action": "CONTINUE"
            },
            "purchase_units": [
                {
                    "reference_id": "{}".format(self.reference_id),
                    "description": "{}".format(self.description),
                    "custom_id": "{}".format(self.custom_id),
                    "soft_descriptor": "{}".format(self.soft_descriptor),
                    "amount": {
                        "currency_code": "{}".format(self.payment_amount.currency_code),
                        "value": "".format(self.payment_amount.amount)
                    }
                }
            ]
        }

    ***REMOVED***This function can be used to create an order with minimum required request body***REMOVED***

    def create_order(self, debug: bool = True):
        ***REMOVED***
               TODO -  from the response take "__approve__" link and redirect the user there, this should be done from the _ipn
        :param debug:
        :return:
        ***REMOVED***
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body(self.build_order_request_body())
        response = self.client.execute(request)
        if debug:
            print('Order With Minimum Payload:')
            print('Status Code:', response.status_code)
            print('Status:', response.result.status)
            print('Order ID:', response.result.id)
            print('Intent:', response.result.intent)
            print('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                                               response.result.purchase_units[0].amount.value))
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))
        self.order_id = response.result.id
        self.order_response = response
        return response

    def get_approve_link(self):
        ***REMOVED***

        :return:
        ***REMOVED***
        if self.order_response:
            for link in self.order_response.result.links:
                if link.rel == "_approve_":
                    return link

    def authorize_order(self, order_id: typing.Union[str, None],  debug: bool = False):
        ***REMOVED***Method to authorize order using order_id***REMOVED***
        if isinstance(order_id, str):
            request = OrdersAuthorizeRequest(order_id)
        else:
            request = OrdersAuthorizeRequest(self.order_id)

        request.prefer("return=representation")
        request.request_body(self.build_order_request_body())
        response = self.client.execute(request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Authorization ID:', response.result.purchase_units[0].payments.authorizations[0].id)
            print('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Authorization Links:')
            for link in response.result.purchase_units[0].payments.authorizations[0].links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print("Buyer:")
            print("\tEmail Address: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
                                                                   response.result.payer.phone.phone_number.national_number))
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))
        self.authorization_id = response.result.purchase_units[0].payments.authorizations[0].id
        self.authorize_response = response
        return response

    ***REMOVED***This function can be used to capture an approved authorization. 
    Valid authorization id should be passed as an argument to this function.***REMOVED***
    def capture_order(self, authorization_id: typing.Union[str, None] = None, debug=False):
        ***REMOVED***Method to capture order using authorization_id***REMOVED***
        if isinstance(authorization_id, str):
            request = AuthorizationsCaptureRequest(authorization_id)
        else:
            request = AuthorizationsCaptureRequest(self.authorization_id)

        request.request_body(capture=self.build_order_request_body())
        response = self.client.execute(request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Capture ID: ', response.result.id)
            print('Links: ')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))
            self.capture_response = response
        return response


class PayPalRecurring(PayPalClient):
    ***REMOVED***
        used to create membership plans
    ***REMOVED***
    name: str = ""
    description: str = ""
    category: str = ""
    image_url: str = ""
    home_url: str = ""

    def __init__(self, app, custom_id: str):
        super(PayPalRecurring, self).__init__(app=app)
        self.custom_id = custom_id

    def set_service_details(self, name: str, description: str, category: str, image_url: str, home_url: str):
        self.name = name
        self.description = description
        self.category = category
        self.image_url = image_url
        self.home_url = home_url

    def build_service_request_body(self) -> dict:
        ***REMOVED***
            creating the body of a recurring payment plan
            :return: dict
        ***REMOVED***
        return {
                   "name": "{}".format(self.name),
                   "description": "{}".format(self.description),
                   "type": "SERVICE",
                   "category": "{}".format(self.category),
                   "image_url": "{}".format(self.image_url),
                   "home_url": "{}".format(self.home_url)
            }

    def create_service(self, debug: bool = False):
        ***REMOVED***
            used to create a new recurring plan
        :return:
        ***REMOVED***
        request = PlansCreateServiceProduct()
        request.prefer(prefer='return=representation')
        request.request_body(service_action_request=self.build_service_request_body())
        # NOTE: the serialize response encoder does support json content- but test this with v1 api
        response = self.client.execute(request)
        if debug:
            print('Product or service for payment plan created:')
            print('Status Code: {}'.format(response.status_code))
            print('Product or Service ID: {}'.format(response.id))
            print('Create_time: {}'.format(response.create_time))
        return response

    def create_plan(self):
        ***REMOVED***
            from a defined service, create the plans needed
            example: Bronze, Gold and Platinum
        :return: created_plan
        ***REMOVED***
        pass

    def activate_plan(self):
        ***REMOVED***
            used to activate recurring payment plans
        :return:
        ***REMOVED***
        pass
