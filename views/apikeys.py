import typing
from flask import jsonify, current_app
from config.exception_handlers import handle_view_errors
from config.exceptions import DataServiceError, status_codes, InputError, error_codes, UnAuthenticatedError
from config.use_context import use_context
from database.organization import OrgValidators, AuthUserValidators
from database.apikeys import APIKeys
from main import app_cache
from utils.utils import create_id, return_ttl, can_cache


class APIKeysValidators(OrgValidators, AuthUserValidators):
    def __init__(self):
        super(APIKeysValidators, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def organization_exist(self, organization_id: typing.Union[str, None]) -> bool:
        ***REMOVED***
            checks if an organization is in existence
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        does_organization_exist: typing.Union[bool, None] = self.is_organization_exist(organization_id=organization_id)
        if isinstance(does_organization_exist, bool):
            return does_organization_exist
        raise DataServiceError(status=500, description="Database Error: Unable to verify organization")

    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def user_can_create_key(self, uid: typing.Union[str, None], organization_id: typing.Union[str, None]) -> bool:
        ***REMOVED***
            checks if user can create key
        :param uid:
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        is_member_of_org: typing.Union[bool, None] = self.user_is_member_of_org(uid=uid, organization_id=organization_id)
        user_is_admin: typing.Union[bool, None] = self.org_user_is_admin(uid=uid, organization_id=organization_id)
        if isinstance(is_member_of_org, bool) and isinstance(user_is_admin, bool):
            return is_member_of_org and user_is_admin
        raise DataServiceError(status=500, description="Database Error: Unable to verify user")


class APIKeysView(APIKeysValidators):
    ***REMOVED***
        a view class for APIKeys
    ***REMOVED***
    def __init__(self):
        super(APIKeysView, self).__init__()

    def _create_unique_api_key(self) -> str:
        _key = create_id()
        api_instance: APIKeys = APIKeys.query(APIKeys.api_key == _key).get()
        return self._create_unique_secret_key() if isinstance(api_instance, APIKeys) else _key

    def _create_unique_secret_key(self) -> str:
        _secret = create_id()
        api_instance: APIKeys = APIKeys.query(APIKeys.secret_token == _secret).get()
        return self._create_unique_secret_key() if isinstance(api_instance, APIKeys) else _secret

    @use_context
    @handle_view_errors
    def create_keys(self, domain: typing.Union[str, None],
                    uid: typing.Union[str, None], organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
                create api_key secret combination
                1. check if organization exist
                2. check if user is member of organization
                3. check if domain is valid
                4. check if users plan allows api_key creation
                5. create api_key secret combination
            :param domain: the domain which will be attached to the API Keys
            :param uid: the user creating the API keys
            :param organization_id: the organization under which the API key will be created
            :return: response containing the API Key and Secret Combination
        ***REMOVED***
        org_exist: bool = self.organization_exist(organization_id=organization_id)
        can_create_key: bool = self.user_can_create_key(uid=uid, organization_id=organization_id)
        if org_exist and can_create_key:
            # create key secret key combo
            api_key: str = self._create_unique_api_key()
            secret_token: str = self._create_unique_secret_key()

            api_key_instance: APIKeys = APIKeys(organization_id=organization_id,
                                                api_key=api_key,
                                                secret_token=secret_token,
                                                assigned_to_uid=uid,
                                                domain=domain,
                                                is_active=True)
            key = api_key_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "database error: unable to create api_key"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "successfully created api_key secret_token combo"
            return jsonify({'status': True, 'payload': api_key_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = 'User not authorized to create keys'
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    @use_context
    @handle_view_errors
    def deactivate_key(self, key: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            # admin only - this will de-activate the API Key rendering it not usable

            :param key: key to de-activate
            :return: deleted api-key
        ***REMOVED***
        if not isinstance(key, str) or not bool(key.strip()):
            message: str = "key is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        api_key_instance: APIKeys = APIKeys.query(APIKeys.key == key).get()
        if isinstance(api_key_instance, APIKeys):
            api_key_instance.is_active = False
            key = api_key_instance.put()
            if not bool(key):
                message: str = "database error: unable to deactivate_key"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "successfully deactivated api_key"
            return jsonify({'status': True, 'payload': api_key_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        return jsonify({'status': False, 'message': 'api key not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def activate_key(self, key: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            admin only function
        :param key: activate a given api-key
        :return:
        ***REMOVED***
        if not isinstance(key, str) or not bool(key.strip()):
            message: str = "key is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        api_key_instance: APIKeys = APIKeys.query(APIKeys.key == key).get()
        if isinstance(api_key_instance, APIKeys):
            api_key_instance.is_active = True
            key = api_key_instance.put()
            if not bool(key):
                message: str = "database error: unable to activate_key"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            message: str = "successfully activated api_key"
            return jsonify({'status': True, 'payload': api_key_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'api key not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_all_organization_keys(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return a list of api-keys belonging to a specific organization
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        api_keys_list: typing.List[APIKeys] = APIKeys.query(APIKeys.organization_id == organization_id).fetch()
        payload: typing.List[dict] = [_key.to_dict() for _key in api_keys_list]

        if len(payload) > 0:
            message: str = 'organization api keys returned successfully'
            return jsonify({'status': True, 'payload': payload, 'message': message}), status_codes.status_ok_code

        message: str = "organization api keys not found"
        return jsonify({'status': False, 'payload': payload, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def return_active_organization_keys(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return_active_organization_keys returns all active organizational keys
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        api_keys_list: typing.List[APIKeys] = APIKeys.query(APIKeys.organization_id == organization_id,
                                                            APIKeys.is_active == True).fetch()
        payload: typing.List[dict] = [_key.to_dict() for _key in api_keys_list]

        if len(payload) > 0:
            message: str = 'organization api keys returned successfully'
            return jsonify({'status': True, 'payload': payload, 'message': message}), status_codes.status_ok_code

        message: str = "organization api keys not found"
        return jsonify({'status': False, 'payload': payload, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_api_key(self, api_key: typing.Union[str, None], organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            fetch a specific api key
        :param api_key:
        :param organization_id:
        :return:
        ***REMOVED***
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(api_key, str) or not bool(api_key.strip()):
            message: str = "api_key is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        api_instance: APIKeys = APIKeys.query(APIKeys.organization_id == organization_id,
                                              APIKeys.api_key == api_key).get()

        if isinstance(api_instance, APIKeys):
            message: str = "successfully fetched api_key record"
            return jsonify({'status': True, 'payload': api_instance.to_dict(),
                            'message': message}), status_codes.status_ok_code

        message: str = "api_key record not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code
