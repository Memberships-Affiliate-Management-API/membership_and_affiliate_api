import typing
from datetime import datetime
from flask import url_for, json
from _sdk._paypal.paypal_client import PayPalClient
from _sdk._paypal.orders import OrdersCreateRequest, OrdersAuthorizeRequest
from _sdk._paypal.payments import AuthorizationsCaptureRequest
from _sdk._paypal.reccuring import PlansCreateServiceProduct
from _sdk._paypal.reccuring.create_plan_request import PlansCreatePlan
from _sdk._paypal.reccuring.create_subscriber_request import PlansCreateSubscriptionRequest
from database.mixins import AmountMixin


class PayPalOrders(PayPalClient):
    """Setting up the complete JSON request body for creating the Order. The Intent in the
        request body should be set as "AUTHORIZE" for capture intent flow."""

    """Setting up the minimum required JSON request body for creating the Order. The Intent in the
        request body should be set as "AUTHORIZE" for capture intent flow."""
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
        """Method to create body with AUTHORIZE intent"""
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
                        "value": "".format(self.payment_amount.amount_cents)
                    }
                }
            ]
        }

    """This function can be used to create an order with minimum required request body"""

    def create_order(self, debug: bool = True):
        """
               TODO -  from the response take "__approve__" link and redirect the user there, this should be done from the _ipn
        :param debug:
        :return:
        """
        create_order_request = OrdersCreateRequest()
        create_order_request.prefer('return=representation')
        create_order_request.request_body(self.build_order_request_body())
        response = self.client.execute(create_order_request)
        if debug:
            print('Order With Minimum Payload:')
            print('Status Code:', response.status_code)
            print('Status:', response.result.payment_status)
            print('Order ID:', response.result.id)
            print('Intent:', response.result.intent)
            print('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount_cents.currency_code,
                                               response.result.purchase_units[0].amount_cents.value))
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))
        self.order_id = response.result.id
        self.order_response = response
        return response

    def get_approve_link(self):
        """

        :return:
        """
        if self.order_response:
            for link in self.order_response.result.links:
                if link.rel == "_approve_":
                    return link

    def authorize_order(self, order_id: typing.Union[str, None],  debug: bool = False):
        """Method to authorize order using order_id"""
        if isinstance(order_id, str):
            auth_order_request = OrdersAuthorizeRequest(order_id)
        else:
            auth_order_request = OrdersAuthorizeRequest(self.order_id)

        auth_order_request.prefer("return=representation")
        auth_order_request.request_body(self.build_order_request_body())
        response = self.client.execute(auth_order_request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.payment_status)
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

    def capture_order(self, authorization_id: typing.Union[str, None] = None, debug=False):
        """
            This function can be used to capture an approved authorization.
            Valid authorization id should be passed as an argument to this function.

            :param authorization_id:
            :param debug:
            :return:
        """

        if isinstance(authorization_id, str):
            capture_request = AuthorizationsCaptureRequest(authorization_id)
        else:
            capture_request = AuthorizationsCaptureRequest(self.authorization_id)

        capture_request.request_body(capture=self.build_order_request_body())
        response = self.client.execute(capture_request)
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.payment_status)
            print('Capture ID: ', response.result.id)
            print('Links: ')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            json_data = self.object_to_json(response.result)
            print("json_data: ", json.dumps(json_data, indent=4))
            self.capture_response = response
        return response


class PayPalRecurring(PayPalClient):
    """
        used to create membership plans
    """
    name: str = ""
    description: str = ""
    category: str = ""
    image_url: str = ""
    home_url: str = ""

    def __init__(self, app, custom_id: str):
        super(PayPalRecurring, self).__init__(app=app)
        self.custom_id = custom_id
        self.debug = app.config.get('DEBUG')

    def set_service_details(self, name: str, description: str, category: str, image_url: str, home_url: str):
        self.name = name
        self.description = description
        self.category = category
        self.image_url = image_url
        self.home_url = home_url

    def build_service_request_body(self) -> dict:
        """
            creating the body of a recurring payment plan
            :return: dict
        """
        return {
                   "name": "{}".format(self.name),
                   "description": "{}".format(self.description),
                   "type": "SERVICE",
                   "category": "{}".format(self.category),
                   "image_url": "{}".format(self.image_url),
                   "home_url": "{}".format(self.home_url)
            }

    @staticmethod
    def build_plan_body(product_id: str, plan_name: str, plan_description: str, plan_amount: AmountMixin,
                        setup_amount: AmountMixin, include_trial: bool = True, interval: str = "MONTH",
                        total_cycles: int = 12, include_taxes: bool = False, tax_percent: int = 15):
        """
                curl -v -k -X POST https://api-m.sandbox.paypal.com/v1/billing/plans \
                  -H "Accept: application/json" \
                  -H "Authorization: Bearer Access-Token" \
                  -H "PayPal-Request-Id: PLAN-18062020-001" \  // merchant generated ID, optional and needed for idempotent samples
                  -H "Prefer: return=representation" \
                  -H "Content-Type: application/json" \

              -d '{
                  "product_id": "PROD-6XB24663H4094933M",
                  "name": "Basic Plan",
                  "description": "Basic plan",
                  "billing_cycles": [
                    {
                      "frequency": {
                        "interval_unit": "MONTH",
                        "interval_count": 1
                      },
                      "tenure_type": "TRIAL",
                      "sequence": 1,
                      "total_cycles": 1
                    },
                    {
                      "frequency": {
                        "interval_unit": "MONTH",
                        "interval_count": 1
                      },
                      "tenure_type": "REGULAR",
                      "sequence": 2,
                      "total_cycles": 12,
                      "pricing_scheme": {
                        "fixed_price": {
                          "value": "10",
                          "currency_code": "USD"
                        }
                      }
                    }
                  ],
                  "payment_preferences": {
                    "auto_bill_outstanding": true,
                    "setup_fee": {
                      "value": "10",
                      "currency_code": "USD"
                    },
                    "setup_fee_failure_action": "CONTINUE",
                    "payment_failure_threshold": 3
                  },
                  "taxes": {
                    "percentage": "10",
                    "inclusive": false
                  }
                }'
        """
        if include_trial:
            return {
                "product_id": "{}".format(product_id),
                "name": "{}".format(plan_name),
                "description": "{}".format(plan_description),
                "billing_cycles": [
                    {
                        "frequency": {
                            "interval_unit": "{}".format(interval),
                            "interval_count": 1
                        },
                        "tenure_type": "TRIAL",
                        "sequence": 1,
                        "total_cycles": 1
                    },
                    {
                        "frequency": {
                            "interval_unit": "{}".format(interval),
                            "interval_count": 1
                        },
                        "tenure_type": "REGULAR",
                        "sequence": 2,
                        "total_cycles": total_cycles,
                        "pricing_scheme": {
                            "fixed_price": {
                                "value": "{}".format(plan_amount.amount_cents),
                                "currency_code": "{}".format(plan_amount.currency)
                            }
                        }
                    }
                ],
                "payment_preferences": {
                    "auto_bill_outstanding": True,
                    "setup_fee": {
                        "value": "{}".format(setup_amount.amount_cents),
                        "currency_code": "{}".format(setup_amount.currency)
                    },
                    "setup_fee_failure_action": "CONTINUE",
                    "payment_failure_threshold": 4
                },
                "taxes": {
                    "percentage": "{}".format(tax_percent),
                    "inclusive": include_taxes
                }
            }

        return {
            "product_id": "{}".format(product_id),
            "name": "{}".format(plan_name),
            "description": "{}".format(plan_description),
            "billing_cycles": [
                {
                    "frequency": {
                        "interval_unit": "{}".format(interval),
                        "interval_count": 1
                    },
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": total_cycles,
                    "pricing_scheme": {
                        "fixed_price": {
                            "value": "{}".format(plan_amount.amount_cents),
                            "currency_code": "{}".format(plan_amount.currency)
                        }
                    }
                }
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee": {
                    "value": "{}".format(setup_amount.amount_cents),
                    "currency_code": "{}".format(setup_amount.currency)
                },
                "setup_fee_failure_action": "CONTINUE",
                "payment_failure_threshold": 4
            },
            "taxes": {
                "percentage": "{}".format(tax_percent),
                "inclusive": include_taxes
            }
        }

    # NOTE: use this function to create a service or product for a membership plan
    def create_service(self):
        """
            used to create a new recurring plan
            If creating a product/service succeeds,
            it triggers the CATALOG.PRODUCT.CREATED webhook.
            #TODO - from this webhook save the plan data
            #The data structure to save the plan data must include the organization_id
        :return:
        """
        service_request = PlansCreateServiceProduct()
        service_request.prefer(prefer='return=representation')
        service_request.request_body(service_action_request=self.build_service_request_body())
        # NOTE: the serialize response encoder does support json content- but test this with v1 api
        response = self.client.execute(service_request)
        if self.debug:
            print('Product or service for payment plan created:')
            print('Status Code: {}'.format(response.status_code))
            print('Product or Service ID: {}'.format(response.result.id))
            print('Create_time: {}'.format(response.result.create_time))
        return response

    # NOTE: use this function to create a service or product plan
    def create_a_plan(self, product_id: str, plan_name: str, plan_description: str, plan_amount: AmountMixin,
                      setup_amount: AmountMixin, include_trial: bool = True, interval: str = "MONTH",
                      total_cycles: int = 0, include_taxes: bool = False, tax_percent: int = 15):

        """
            from a defined service, create the plans needed
            example: Basic Plan,Standard and Premium
            /v1/billing/plans
            Plans are active by default.

            For quantity (user or seat) based pricing plans,
            set the quantity_supported attribute to true to indicate that customers can
            subscribe to this plan by providing the number of units they what to subscribe to.
            (eg. web hosting services)

            If creating a plan succeeds, it triggers the BILLING.PLAN.CREATED webhook.
            :return: created_plan
        """

        plan_request = PlansCreatePlan()
        plan_request.prefer(prefer='return=representation')

        plan_request.request_body(service_action_request=self.build_plan_body(
            product_id=product_id, plan_name=plan_name, plan_description=plan_description,
            plan_amount=plan_amount, setup_amount=setup_amount, include_trial=include_trial,
            interval=interval, total_cycles=total_cycles, include_taxes=include_taxes,
            tax_percent=tax_percent))

        response = self.client.execute(plan_request)
        # NOTE: If creating a plan succeeds, it triggers the BILLING.PLAN.CREATED webhook.
        if self.debug:
            print("Create a Finite Plan")
            print("Plan ID: {}".format(response.result.id))
            print("Product ID: {}".format(response.result.product_id))
            print("Plan Name: {}".format(response.result.name))
            print("Status: {}".format(response.result.payment_status))
            print("LINKS : ")
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))

        return response

    # NOTE: Create a subscription Body this assumes an active plan already exists to subscribe the user
    # NOTE: to, the API will recognize to whom the plan belong to through the Memberships Module

    @staticmethod
    def create_subscription_body(plan_id: str, start_time: datetime, name: str, surname: str,
                                 paypal_email_address: str, brand_name: str,
                                 return_url: str, cancel_url: str,  locale: str = "en-US"):
        return {
                  "plan_id": "{}".format(plan_id),
                  "start_time": "{}".format(start_time),
                  "subscriber": {
                    "name": {
                      "given_name": "{}".format(name),
                      "surname": "{}".format(surname)
                    },
                    "email_address": "{}".format(paypal_email_address)
                  },
                  "application_context": {
                    "brand_name": "{}".format(brand_name),
                    "locale": "{}".format(locale),
                    "shipping_preference": "SET_PROVIDED_ADDRESS",
                    "user_action": "SUBSCRIBE_NOW",
                    "payment_method": {
                      "payer_selected": "PAYPAL",
                      "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                    },
                    "return_url": "{}".format(return_url),
                    "cancel_url": "{}".format(cancel_url)
                  }
            }

    # NOTE: Call this function to subscribe users to an existing and active plan
    # NOTE: on success redirect users to an authorize screen users will authorize the subscription
    # NOTE:  and we are done
    def create_subscription(self, plan_id: str, start_time: datetime, name: str, surname: str,
                            paypal_email_address: str, brand_name: str,
                            return_url: str, cancel_url: str,  locale: str = "en-US"):
        """
            Subscriptions with Smart Payment Buttons
                To use Subscriptions with Smart Payment Buttons:

                1. Add the PayPal script to your web page.
                2. Render the Smart Payment Button.
                3. Create the subscription.
            Add the PayPal script
                Add the PayPal script to your web page and add your sandbox client_id to the script tag.


                <!DOCTYPE html>

                <head>
                  <meta name="viewport" content="width=device-width, initial-scale=1">
                  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                </head>

                <body>
                  <script
                      src="https://www.paypal.com/sdk/js?client-id=SB_CLIENT_ID&vault=true&intent=subscription">
                  </script>
                </body>

            client-id	test	required	Your PayPal REST client ID. This identifies your
            PayPal account and determines where transactions are paid to.
            While you're testing in sandbox, you can use client-id=test as a shortcut.

            vault	true, false	false	Set to true for subscriptions.

            intent	capture, authorize, subscription, tokenize	capture	Set to subscription
            for subscriptions

            Next Step

            Render the Smart Payment Button
            Next, render the PayPal Smart Payment Buttons to a container element on your page.

            <script
                src="https://www.paypal.com/sdk/js?client-id=SB_CLIENT_ID&vault=true&intent=subscription">
            </script>

            <div id="paypal-button-container"></div>

            <script>
                paypal.Buttons().render('#paypal-button-container');
            </script>



            Create the subscription
                Finally, implement the createSubscription function that's called when the buyer
                clicks the PayPal button. This function:

                Calls PayPal using actions.subscription.create() to create a subscription for
                your plan and includes the plan ID, subscriber details, shipping,
                and other details.

                Launches the PayPal subscription window so the buyer can log in and approve the
                subscription on www.paypal.com.


                paypal.Buttons({

                  createSubscription: function(data, actions) {

                    return actions.subscription.create({

                      'plan_id': 'P-2UF78835G6983425GLSM44MA'

                    });

                  },


                  onApprove: function(data, actions) {

                    alert('You have successfully created subscription ' + data.subscriptionID);

                  }


                }).render('#paypal-button-container');

            :return: created plan with an indeterminate cycle

            # NOTE Subscriber Flow

            curl -v -k -X POST https://api-m.sandbox.paypal.com/v1/billing/subscriptions \
               -H "Accept: application/json" \
               -H "Authorization: Bearer Access-Token" \
               -H "PayPal-Request-Id: SUBSCRIPTION-21092020-001" \
               -H "Prefer: return=representation" \
               -H "Content-Type: application/json" \
               -d '{
                  "plan_id": "P-2UF78835G6983425GLSM44MA",
                  "start_time": "2020-02-27T06:00:00Z",
                  "subscriber": {
                    "name": {
                      "given_name": "John",
                      "surname": "Doe"
                    },
                    "email_address": "customer@example.com"
                  },
                  "application_context": {
                    "brand_name": "example",
                    "locale": "en-US",
                    "shipping_preference": "SET_PROVIDED_ADDRESS",
                    "user_action": "SUBSCRIBE_NOW",
                    "payment_method": {
                      "payer_selected": "PAYPAL",
                      "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                    },
                    "return_url": "https://example.com/returnUrl",
                    "cancel_url": "https://example.com/cancelUrl"
                  }
                }'        
        """

        subscription_request = PlansCreateSubscriptionRequest()
        subscription_request.prefer(prefer='return=representation')
        subscription_request.request_body(service_action_request=self.create_subscription_body(
            plan_id=plan_id, start_time=start_time, name=name, surname=surname,
            paypal_email_address=paypal_email_address, brand_name=brand_name, return_url=return_url,
            cancel_url=cancel_url, locale=locale))
        response = self.client.execute(subscription_request)
        if self.debug:
            print("Creating Subscriptions")
            print("Subscription ID: {}".format(response.result.id))
            print("Plan_ID: {}".format(response.result.plan_id))
            print("Start Time: {}".format(response.result.start_time))
            print("Create Time: {}".format(response.result.create_time))
            print("STATUS : {}".format(response.result.payment_status))
            print("STATUS UPDATE TIME: {}".format(response.results.status_update_time))
            print("Subscription Link :")

            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))

        # NOTE: the user must be redirected to the approve link in order to approve the plan
        # link rel : "approve"
        # NOTE: If creating a subscription succeeds, it triggers the BILLING.SUBSCRIPTION.CREATED webhook
        # NOTE: When a subscription has been paid using auto debit, it triggers the PAYMENT.SALE.COMPLETED webhook.
        # Redirect User here to approve GET https://www.paypal.com/webapps/billing/subscriptions?ba_token={BA-Token-ID}
        return response
