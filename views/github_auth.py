***REMOVED***
    **github authentication module**
        allows clients to gain access to the api dashboard through github authorization
***REMOVED***
import json
import requests
from flask import current_app, jsonify
from typing import Optional, List
from google.cloud import ndb
from config.exception_handlers import handle_view_errors
from config.exceptions import InputError, error_codes, DataServiceError, status_codes
from config.use_context import use_context
from database.users import GithubUser
from utils import create_id


class Validators:
    ***REMOVED***
        **Utilities and Validators for GithubAuthView Class**
    ***REMOVED***
    def __init__(self):
        self._admin_check_user_endpoint = "_api/admin/users/is-user-unique"
        self._base_url = current_app.config.get('BASE_URL')
        self._user_dict: Optional[dict] = None

    def account_lookup(self, email: str) -> Optional[str]:
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
        response, status = requests.post(url=_url, json=json.dumps(dict(email=email)))
        user_instance_dict: dict = response.to_dict()

        # NOTE: if user is found it means there is a user with this record -
        # then return the uid of this user
        # TODO insure that one user can belong to multiple organizations with a single uid
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
        response, status = requests.post(url=_url, json=json.dumps(dict(uid=_uid)))
        user_instance_dict: dict = response.to_dict()
        # if user not found then this means there is no user with such an ID
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
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
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

        # NOTE: the users registration here is for the client dashboard section only
        # hence this is why we are using the organization_id of the main app
        organization_id: Optional[str] = current_app.get('organization_id')

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

        github_user_instance: GithubUser = GithubUser(
            uid=uid, organization_id=organization_id, access_token=access_token, email=email,
            twitter_username=twitter_username, github_name=github_name, avatar_url=avatar_url, api_url=api_url,
            html_url=html_url, following_url=following_url, followers_url=followers_url, gists_url=gists_url,
            repos_url=repos_url)

        key: Optional[ndb.Key] = github_user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            message: str = "Database Error: while creating new User"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        message: str = "Successfully created new user"
        return jsonify({'status': True, 'payload': github_user_instance.to_dict(),
                        'message': message}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def update_user(self, user_details: dict) -> tuple:
        ***REMOVED***

        :param user_details:
        :return:
        ***REMOVED***
        email: Optional[str] = user_details.get('email')
        if not isinstance(email, str) or not bool(email.strip()):
            message: str = 'Email is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        uid: Optional[str] = user_details.get('uid')
        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # TODO create a function to get this data
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

        github_user_instance: Optional[GithubUser] = GithubUser.query(
            GithubUser.uid == GithubUser.uid, GithubUser.organization_id == organization_id).get()

        if isinstance(github_user_instance, GithubUser):
            github_user_instance.email = email
            github_user_instance.twitter_username = twitter_username
            github_user_instance.github_name = github_name
            github_user_instance.access_token = access_token
            github_user_instance.avatar_url = avatar_url
            github_user_instance.api_url = api_url
            github_user_instance.html_url = html_url
            github_user_instance.followers_url = followers_url
            github_user_instance.following_url = following_url
            github_user_instance.gists_url = gists_url
            github_user_instance.repos_url = repos_url

            key: Optional[ndb.Key] = github_user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not isinstance(key, ndb.Key):
                message: str = "Database Error: Unable to update github user"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # TODO - update cache_manager
            message: str = "successfully updated user"
            return jsonify({'status': True,
                            'payload': github_user_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code
        message: str = "user not found: Unable to update user"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def delete_user(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        ***REMOVED***

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        pass

    @use_context
    @handle_view_errors
    def get_user(self, organization_id: Optional[str], uid: Optional[str]) -> tuple:
        ***REMOVED***

        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = 'uid is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        github_user_instance: GithubUser = GithubUser.query(GithubUser.organization_id == organization_id,
                                                            GithubUser.uid == uid).get()
        if isinstance(github_user_instance, GithubUser):
            message: str = 'user record found'
            return jsonify({'status': True, 'payload': github_user_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        message: str = 'Unable to find user'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def return_organization_users(self, organization_id: Optional[str]) -> tuple:
        ***REMOVED***

        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        github_users: List[dict] = [user.to_dict() for user in GithubUser.query(
            GithubUser.organization_id == organization_id)]
        if isinstance(github_users, list) and len(github_users):
            message: str = 'users successfully fetched'
            return jsonify({'status': True, 'payload': github_users,
                            'message': message}), status_codes.status_ok_code

        message: str = "user not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code
