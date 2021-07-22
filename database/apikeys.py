from google.cloud import ndb
from database.setters import setters


class APIKeys(ndb.Model):
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    api_key: str = ndb.StringProperty(validator=setters.set_id)
    secret_token: str = ndb.StringProperty(validator=setters.set_id)
    assigned_to_uid: str = ndb.StringProperty(validator=setters.set_id)
    domain: str = ndb.StringProperty(validator=setters.set_domain)
    is_active: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)
    # admin, support, user
    access_control: list = ndb.StringProperty(repeated=True)

    def __str__(self) -> str:
        return "APIKeys: Organization: {}, key: {} ".format(self.organization_id, self.api_key)

    def __repr__(self) -> str:
        return self.__str__()

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

    def __len__(self) -> int:
        return 1 if self.__bool__() else 0





