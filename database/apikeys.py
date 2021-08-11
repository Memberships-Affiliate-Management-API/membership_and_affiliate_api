***REMOVED***
    ** Affiliates Keys Module**
    definition of classes to handle APIKeys for client authorization

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from google.cloud import ndb
from database.setters import property_
from database.basemodel import BaseModel


class APIKeys(BaseModel):
    ***REMOVED***
        **Class APIKeys**
            a class to keep track of all api keys created for clients / organization in order to access our API
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=property_.set_id, indexed=True, required=True)
    api_key: str = ndb.StringProperty(validator=property_.set_id, indexed=True, required=True)
    secret_token: str = ndb.StringProperty(validator=property_.set_id, indexed=True, required=True)
    assigned_to_uid: str = ndb.StringProperty(validator=property_.set_id, indexed=True, required=True)
    domain: str = ndb.StringProperty(validator=property_.set_domain, indexed=True, required=True)
    is_active: bool = ndb.BooleanProperty(default=True, validator=property_.set_bool)

    def __str__(self) -> str:
        return "APIKeys: Organization: {}, key: {} ".format(self.organization_id, self.api_key)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.api_key != other.api_key:
            return False
        if self.secret_token != other.secret_token:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.api_key)
