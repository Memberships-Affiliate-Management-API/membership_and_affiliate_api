***REMOVED***
    **Affiliate API Endpoint**

    module intended as an Affiliate Api Route for clients using memberships and affiliate management api
    the module handles routing api requests and authentication of each call
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"


import typing
from flask import Blueprint, request
from config.exceptions import if_bad_request_raise
from security.api_authenticator import handle_api_auth
from views.affiliates import AffiliatesView, RecruitsView

affiliates_bp = Blueprint('affiliates', __name__)


# NOTE: there is no reason to cache API routes as the cache is on the view level
@affiliates_bp.route('/api/v1/affiliate/<path:path>', methods=['POST'])
@handle_api_auth
def affiliate(path: str) -> tuple:
    ***REMOVED***
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

    ***REMOVED***
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)
    affiliate_view_instance: AffiliatesView = AffiliatesView()
    affiliate_data: dict = request.get_json()

    # TODO - include organization_id for this routes

    if path == "get":
        # Note response may be cached by the view function
        return affiliate_view_instance.get_affiliate(affiliate_data=affiliate_data)
    elif path == "get-all":
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')
        return affiliate_view_instance.get_all_affiliates(organization_id=organization_id)
    elif path == "get-active":
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')
        return affiliate_view_instance.get_active_affiliates(organization_id=organization_id)
    elif path == "get-not-active":
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')
        return affiliate_view_instance.get_in_active_affiliates(organization_id=organization_id)
    elif path == "get-deleted":
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')
        return affiliate_view_instance.get_deleted_affiliates(organization_id=organization_id)
    elif path == "get-not-deleted":
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')
        return affiliate_view_instance.get_not_deleted_affiliates(organization_id=organization_id)
    elif path == "register":
        return affiliate_view_instance.register_affiliate(affiliate_data=affiliate_data)
    elif path == "inc-recruits":
        return affiliate_view_instance.total_recruits(affiliate_data=affiliate_data, add=1)
    elif path == 'dec-recruits':
        return affiliate_view_instance.total_recruits(affiliate_data=affiliate_data, add=-1)
    elif path == 'delete':
        return affiliate_view_instance.delete_affiliate(affiliate_data=affiliate_data)
    elif path == 'mark-active':
        return affiliate_view_instance.mark_active(affiliate_data=affiliate_data, is_active=True)
    elif path == 'mark-not-active':
        return affiliate_view_instance.mark_active(affiliate_data=affiliate_data, is_active=False)


@affiliates_bp.route('/api/v1/recruits/<path:path>', methods=['POST'])
@handle_api_auth
def recruits(path: str) -> tuple:
    ***REMOVED***
        **recruits**
            Allows Users and Clients to recruit other users and clients to
            their organizations.

        **PATH PARAMETERS**
            1. get -> retrieve a single recruit, expects organization_id and affiliate_id on recruit_data,
               user may supply the data as json body

            2. register -> used to register a single recruit, data as json must contain referrer_uid and
               organization_id, this allows multiple ways by which recruiters may recruit their affiliates

            3. delete -> soft delete a recruit by affiliate_id , organization_id is required

            4. activate -> mark recruit as active  : required parameters organization_id and affiliate_id

            5. de-activate -> de-activate recruit : required parameters organization_id and affiliate_id

            6. get-active -> returns active recruits : required parameters organization_id

            7. get-in-active -> get in-active recruits : required parameters organization_id

            # TODO finish documentation

    :param path: route to retrieve
    :return:
    ***REMOVED***
    # Raises Bad Request error if request is not in json format
    if_bad_request_raise(request)

    recruits_view_instance: RecruitsView = RecruitsView()
    recruit_data: dict = request.get_json()
    if path == "get":
        # retrieve a single recruit, function expects organization_id and
        # affiliate_id on recruit_data, user may supply the data as json body
        return recruits_view_instance.get_recruit(recruit_data=recruit_data)

    elif path == "register":
        # Note: used to register a single recruit, data as json must contain
        # referrer_uid and organization_id, this allows multiple ways by which
        #  recruiters may recruit their affiliates
        return recruits_view_instance.add_recruit(recruit_data=recruit_data)

    elif path == "delete":
        # Soft Delete a recruit by affiliate_id
        return recruits_view_instance.delete_recruit(recruit_data=recruit_data)
    elif path == "activate":
        return recruits_view_instance.mark_active(recruit_data=recruit_data, is_active=True)
    elif path == "de-activate":
        return recruits_view_instance.mark_active(recruit_data=recruit_data, is_active=False)
    elif path == "get-active":
        return recruits_view_instance.get_recruits_by_active_status(recruit_data=recruit_data, is_active=True)
    elif path == "get-in-active":
        return recruits_view_instance.get_recruits_by_active_status(recruit_data=recruit_data, is_active=False)
    elif path == "get-deleted":
        return recruits_view_instance.get_recruits_by_deleted_status(recruit_data=recruit_data, is_deleted=True)
    elif path == "get-not-deleted":
        return recruits_view_instance.get_recruits_by_deleted_status(recruit_data=recruit_data, is_deleted=False)
    elif path == "get-by-affiliate":
        return recruits_view_instance.get_recruits_by_affiliate(affiliate_data=recruit_data)
    elif path == "get-by-active-affiliate":
        return recruits_view_instance.get_recruits_by_active_affiliate(affiliate_data=recruit_data, is_active=True)
    elif path == "get-by-not-active-affiliate":
        return recruits_view_instance.get_recruits_by_active_affiliate(affiliate_data=recruit_data, is_active=False)
    else:
        pass

    # TODO Fully integrate the Affiliate API to the Admin App
