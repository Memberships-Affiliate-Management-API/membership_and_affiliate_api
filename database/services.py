***REMOVED***
    Services Module works together with memberships module
    for example for a music streaming service a plan will be created
    in MembershipsPlans in the Memberships Module and also
    on PayPal, when a user subscribes to a plan the subscription
    will be created both on Memberships Module and also on PayPal
    so that the subscription amount can be taken off the user paypal_address

***REMOVED***
import typing
from google.cloud import ndb
from config.exceptions import DataServiceError
from database.setters import setters
from database.organization import OrgValidators, AuthUserValidators
from database.users import UserValidators
from main import app_cache
from utils.utils import return_ttl


class ServiceValidator(OrgValidators, AuthUserValidators, UserValidators):
    def __init__(self):
        super(ServiceValidator, self).__init__()

    @app_cache.cached(timeout=return_ttl(name='short'))
    def can_create_service(self, uid: typing.Union[str, None],
                           organization_id: typing.Union[str, None] ) -> typing.Union[None, bool]:

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
        The Services Module, will capture the service data
        the information here will be similar to the information
        on paypal services or products for plans.
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    # NOTE: service_id is the same as product_id in paypal products
    created_by_uid: str = ndb.StringProperty(validator=setters.set_id)
    # NOTE: created_by_uid is the user id of the user who created the service
    service_id: str = ndb.StringProperty(validator=setters.set_id)
    name: str = ndb.StringProperty(validator=setters.set_string)
    description: str = ndb.StringProperty(validator=setters.set_string)
    category: str = ndb.StringProperty(validator=setters.set_string)
    image_url: str = ndb.StringProperty(validator=setters.set_domain)
    # NOTE: home_url is the location online of the page containing
    # the service information page
    home_url: str = ndb.StringProperty(validator=setters.set_domain)

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
