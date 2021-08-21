#### Affiliates API Documentations 

    **affiliate**
        returns information to clients / users relating to affiliates management
        required parameter is organization_id must be a part of the request body supplied as json

    **PARAMETERS**
        :param path: path indicating the resource to return
        :return: response as tuple of Response and Status code

        path == "get"
            this obtains a record of one affiliate from the database the required valuables must be passed in
            json format as a body of a request in this format
            the required variables are as follows:
            organization_id : required
            and either affiliate_id or uid - this means the affiliate record can be obtained by either providing
            an affiliate_id or uid.

        path == "get-all"
            **Method: POST**
            **Body: {"organization_id": "x"} as json**
            fetches all affiliate records belonging to an organization indicated by the supplied
            parameter organization_id.
            organization_id : must be passed in json format as a body of the request

        path == "get-active"
            **Method: POST**
            **BODY: {"organization_id": "value"} as json** required
            fetches active affiliate records belonging to a specific organization,
            organization_id must be specified in the call as json body

        path == "get-not-active"
            **Method: POST**
            **BODY: {"organization_id": "value"} as json** required
            returns in-active affiliate records for your organization

        path == "get-deleted"

        # TODO finish documentation
