***REMOVED***
    **github authentication module**
        allows clients to gain access to the api dashboard through github authorization
***REMOVED***
import json

import requests
from flask import current_app
from typing import Optional
from config.exceptions import InputError, error_codes
from config.use_context import use_context
from database.users import GithubUser
from utils import create_id


class Validators:
    def __init__(self):
        self._admin_check_user_endpoint = "_api/admin/users/is-user-unique"
        self._base_url = current_app.config.get('BASE_URL')
        self._user_dict: Optional[dict] = None

    def account_lookup(self, email: str) -> Optional[str, None]:
        ***REMOVED***
            **does_account_exist**
                if the account with email address already exists on the users - records return the account uid
                if not then return create a new uid and return it
        :param email: email address used to lookup account details
        :return:
        ***REMOVED***

        if self._user_dict and self._user_dict.get('email') == email.lower().strip():
            return self._user_dict.get('uid')

        _url: str = "{}{}".format(self._base_url, self._admin_check_user_endpoint)
        response, _ = requests.post(url=_url, json=json.dumps(dict(email=email)))
        user_instance_dict: dict = response.to_dict()
        if user_instance_dict['status']:
            self._user_dict = user_instance_dict
            return self._user_dict.get('uid')
        return None

    def create_unique_id(self) -> str:
        ***REMOVED***
            **create_unique_id**
                creates a unique user id

        :return:
        ***REMOVED***
        _uid: str = create_id()
        _url: str = "{}{}".format(self._base_url, self._admin_check_user_endpoint)
        response, _ = requests.post(url=_url, json=json.dumps(dict(uid=_uid)))
        user_instance_dict: dict = response.to_dict()
        if not user_instance_dict['status']:
            return _uid
        self.create_unique_id()


class GithubAuthView(Validators):
    ***REMOVED***
        **Class GithubAuthView**
            view controller for github authorization for the client portal

    ***REMOVED***
    def __init__(self):
        super(GithubAuthView, self).__init__()

    @use_context
    def create_user(self, user_details: dict) -> tuple:
        ***REMOVED***
            **create_user**
                gets user details from user_details dict and then create a new user
        :param user_details:
        :return:
        ***REMOVED***
        email: Optional[str] = user_details.get('email')
        if not isinstance(email, str) or not bool(email.strip()):
            message: str = 'Email is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        # Note: if user already registered on the app their account is attached to this login
        uid: Optional[str] = self.account_lookup(email=email)
        if not isinstance(uid, str) or not bool(uid.strip()):
            # TODO need to find a way to update the user record or let the user do it
            uid: str = self.create_unique_id()

        organization_id: Optional[str] = user_details.get('organization_id')
        access_token: Optional[str] = user_details.get('access_token')
        twitter_username: Optional[str] = user_details.get('twitter_username')
        github_name: Optional[str] = user_details.get('github_name')
        avatar_url: Optional[str] = user_details.get('avatar_url')
        api_url: Optional[str] = user_details.get('api_url')
        html_url: Optional[str] = user_details.get('html_url')
        followers_url: Optional[str] = user_details.get('followers_url')
        following_url: Optional[str] = user_details.get('following_url')
        gists_url: Optional[str] = user_details.get('gists_url')
        repos_url: Optional[str] = user_details.get('repos_url')







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

