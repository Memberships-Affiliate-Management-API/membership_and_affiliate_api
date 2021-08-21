#### Coupons API
    Allows developers to intergrate coupon codes functionality into 
    the payment plans for services on their website.
    
#### Endpoints - Details
        **coupons endpoint**
            Allows developers to integrate coupon codes functionality into
            the payment plans for services on their website.
        **PARAMETERS**
            :param path: str -> path that indicates the resource to access
            :return tuple: response, status_code -> tuple containing response (in json format) and status_code

            path == "get"
                given organization_id and coupon_code return coupon code details

            path == "create":
                given organization_id, code, discount, expiration_time , create a new coupon

            path == "update":
                given organization_id, code, discount, and expiration_time update coupon code

            path == "cancel":
                given organization_id and code cancel coupon code

            path == "get-all":
                given organization_id return all coupon codes relevant to the organization.

            path == "get-valid":
                given organization_id return valid coupon codes

            path == "get-expired":
                given organization_id return expired coupon codes

