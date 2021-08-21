**create memberships plan**
   
       this allows developers to create a membership payment plan for an existing service 
       so clients can subscribe to the service by selecting the described payment plan.
   
    **NOTE**
   
        The service or product under which the payment plan is to be created must already 
        be created, in order for you to know which service_id to use to create the payment plan.
   
        Once you successfully created a service or product a service_id will be return which 
        can then be used here to create payment plans
   
    **Endpoint**     
   
        url : https://memberships-affiliates-man-api.herokuapp.com/api/v1/public/membership-plan
    
    **Example**
   
        see code below 
   
   ```javascript
   {
    method = 'POST',
    body = JSON.stringify({ 
            "organization_id": "98asd98asj8df9as8hfa9sd9787fd",
            "service_id": "342kjdh98d982u9384j23jd2d23",
            "plan_name": "beginner",
            "description": "Entry level plan",
            "schedule_day": 1,
            "schedule_term": "monthly",
            "term_payment": 15,
            "registration_amount": 5,
            "currency": "USD"}),
    headers = {'content-type': 'application/json'}       
   }
   ```
   

    returns 
    
    _on success_

    ```javascript 
        {
            "status": true,
            "payload": {
                "organization_id": "98asd98asj8df9as8hfa9sd9787fd",
                "plan_id": "fdfs7dy8fy74h83y58347yrfy87y435",
                "plan_name": "beginner",
                "description": "Entry level plan",
                "schedule_day": 1,
                "schedule_term": "monthly",
                "term_payment": 15,
                "registration_amount": 5,
                "currency": "USD"},
            "message": "successfully created payment plan"
        },
        status_code = 201
    ```

    _on failure_ 
    
    ```javascript 
        {
            "status": false,
            "message": "failed to create payment plan"
        },
        status_code: relevant error code
    ```
