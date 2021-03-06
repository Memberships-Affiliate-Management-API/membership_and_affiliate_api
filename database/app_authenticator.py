"""
    **Micro Services Authenticator database**
        this will be useful when the applications / micro-services making up this api are running on multiple
        cloud providers. or on heroku.

"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from google.cloud import ndb
from database.basemodel import BaseModel


class MicroAuthDetails(BaseModel):
    """
        **Class MicroAuthDetails**
            used to authenticate micro-services requests

    """
    app_id: str = ndb.StringProperty()
    domain: str = ndb.StringProperty()
    secret_key: str = ndb.StringProperty()
    auth_token: str = ndb.StringProperty()

    def __str__(self) -> str:
        """

        :return:
        """
        return f"<MicroAuthDetails: app_id: {self.app_id}, domain: {self.domain}, secret_key: {self.secret_key}, " \
               f"auth_token: {self.auth_token}"

    def __eq__(self, other) -> bool:
        """
            **__eq__**
                checks if two instances are equal

        :param other: an instance to compare with
        :return: bool -> True if Equal
        """
        if self.__class__ != other.__class__:
            return False
        if self.app_id != other.app_id:
            return False
        if self.secret_key != other.secret_key:
            return False
        if self.auth_token != other.auth_token:
            return False
        return True

    def __bool__(self) -> bool:
        """
            **__bool__**
                returns True if valid instance of MicroAuthDetails
        :return: True if Instance
        """
        return bool(self.domain) and bool(self.secret_key) and bool(self.app_id)
