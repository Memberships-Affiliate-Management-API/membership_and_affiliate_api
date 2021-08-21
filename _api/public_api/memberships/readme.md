#### Memberships API 
    The Memberships API simply allows developers to create services on their websites or blogs which can only 
    be accessible when a user becomes a paid or free member (creates subscription) of such a service or product. 
    
    Therefore the Memberships API Allows developers to 
        1. create and describe a service or product
        2. add several subscriptions or payment plans to the service or product
        3. manage clients subscriptions and payment collections for the services and products
    
    The Memberships API is reliant on paypal services for payment collections, so your clients can safely 
    subscribe through paypal to your services and or products.


#### Endpoints Definitions
    for endpoint documentations see relevant readme files below.

1. **create memberships plan**
   this allows developers to create a membership payment plan for an existing service 
   so clients can subscribe to the service by selecting the described payment plan.
   
    **NOTE**
        The service or product under which the payment plan is to be created must already 
        be created, in order for you to know which service_id to use to create the payment plan.
   
        Once you successfully created a service or product a service_id will be return which 
        can then be used here to create payment plans
        
    url = https://memberships-affiliates-man-api.herokuapp.com/api/v1/public/membership-plan

   ```javascript
    method = 'POST'
    body = JSON.stringify({ 
            'organization_id': "98asd98asj8df9as8hfa9sd9787fd",
            'service_id': "342kjdh98d982u9384j23jd2d23",
            'plan_name': "beginner",
            'description': "Entry level plan",
            'schedule_day': 1,
            'schedule_term': "monthly",
            'term_payment': 15,
            'registration_amount': 5,
            'currency': "USD"})
   ```
   