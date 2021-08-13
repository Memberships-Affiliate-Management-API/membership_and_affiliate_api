***REMOVED***
    **github authentication module**
        allows clients to gain access to the api dashboard through github authorization
***REMOVED***
from typing import Optional

from database.users import GithubUser


class GithubAuthView:

    def create_user(self, user_details: dict) -> tuple:
        ***REMOVED***
            **create_user**
                gets user details from user_details dict and then create a new user
        :param user_details:
        :return:
        ***REMOVED***
        pass

    def update_user(self, user_details: dict) -> tuple:
        ***REMOVED***

        :param user_details:
        :return:
        ***REMOVED***
        pass

    def delete_user(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        ***REMOVED***

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        pass

    def get_user(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        ***REMOVED***

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        pass

    def return_organization_users(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***

        :param organization_id:
        :return:
        ***REMOVED***
        pass

