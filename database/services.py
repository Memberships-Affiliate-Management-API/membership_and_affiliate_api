***REMOVED***
    **Services Module**
    Services Module works together with memberships module
    for example for a music streaming service a plan will be created
    in MembershipsPlans in the Memberships Module and also
    on PayPal, when a user subscribes to a plan the subscription
    will be created both on Memberships Module and also on PayPal
    so that the subscription amount can be taken off the user paypal_address

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from datetime import datetime

from google.cloud import ndb
from config.exceptions import DataServiceError
from database.setters import property_
from database.organization import OrgValidators, AuthUserValidators
from database.users import UserValidators
from main import app_cache
from utils.utils import return_ttl


class ServiceValidator(OrgValidators, AuthUserValidators, UserValidators):
    ***REMOVED***
        **Service Class Validator Methods**
            validates services

    ***REMOVED***
    def __init__(self):
        super(ServiceValidator, self).__init__()

    @app_cache.memoize(timeout=return_ttl('short'))
    def can_create_service(self, uid: typing.Union[str, None],
                           organization_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        ***REMOVED***
            **can_create_service**
                checks if user can create a new service if this is the case then returns True
                will raise a DataServiceError if it fails to determine the users ability to create the service

        :param uid:
        :param organization_id:
        :return: boolean indicating if user can create a service
        ***REMOVED***

        # NOTE: Organization has to be valid itself
        org_exist: typing.Union[None, bool] = self.is_organization_exist(organization_id=organization_id)
        # NOTE: only members of the organization administrator group can create services for a plan
        is_admin: typing.Union[None, bool] = self.user_is_member_of_org(uid=uid, organization_id=organization_id)
        # NOTE: de activated users cannot add services
        is_user_valid: typing.Union[None, bool] = self.is_user_valid(uid=uid)

        if isinstance(org_exist, bool) and isinstance(is_admin, bool) and isinstance(is_user_valid, bool):
            return org_exist and is_admin and is_user_valid

        message: str = "Database Error: Unable to verify if user can create service"
        raise DataServiceError(status=500, description=message)


class Services(ndb.Model):
    ***REMOVED***
        **Service Class Documentations**
            **The Services Module**, will capture the service data
            the information here will be similar to the information
            on paypal services or products for payment plans.

            **Products / Services** must be created and stored on paypal before Memberships Payment Plans can be defined

        `Class Properties`
            1. organization_id : the organization which owns the id
            2. created_by_uid: teh person who created the product or service
            3. service_id: the id of the created service - this id comes from paypal
            4. name: name of the service or product
            5. description: description of the product or service
            6. category: category of the product or service
            7. image_url:  image related to product or service - this image could be stored in firebase - or on another endpoint locally on heroku
            8. home_url:  the home url of the page containing this service or product on the client website or blog
            10. date_created: datetime -> the date the service was created
            11. date_updated: datetime -> the date of the last update

        `Method Properties`
            1. service_details: dict -> returns basic service details
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=property_.set_id)
    # NOTE: service_id is the same as product_id in paypal products
    created_by_uid: str = ndb.StringProperty(validator=property_.set_id)
    # NOTE: created_by_uid is the user id of the user who created the service
    service_id: str = ndb.StringProperty(validator=property_.set_id)
    name: str = ndb.StringProperty(validator=property_.set_string)
    description: str = ndb.StringProperty(validator=property_.set_string)
    category: str = ndb.StringProperty(validator=property_.set_string)
    image_url: str = ndb.StringProperty(validator=property_.set_domain)
    # NOTE: home_url is the location online of the page containing
    # the service information page
    home_url: str = ndb.StringProperty(validator=property_.set_domain)
    date_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    date_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.organization_id != other.organization_id:
            return False
        if self.service_id != other.service_id:
            return False
        return True

    def __str__(self) -> str:
        return "<Service name: {}, description: {}, category: {}".format(self.name,
                                                                         self.description,
                                                                         self.category)

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return bool(self.service_id)

    def __len__(self) -> int:
        return int(self.__bool__())

    @property
    def service_details(self) -> dict:
        ***REMOVED***
            `Service Details Property`
                returns basic details for this service i.e organization_id, service_id, name, description, image_url, home_url

        :return: dict -> containing  organization_id, service_id, name, description, image_url, home_url
        ***REMOVED***
        return {
            'organization_id': self.organization_id,
            'service_id': self.service_id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'home_url': self.home_url}
