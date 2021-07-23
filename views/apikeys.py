import typing
from flask import jsonify
from config.exception_handlers import handle_view_errors
from config.exceptions import DataServiceError
from config.use_context import use_context
from database.organization import OrgValidators, AuthUserValidators
from database.apikeys import APIKeys
from main import cache_affiliates
from utils.utils import create_id, return_ttl


class APIKeysValidators(OrgValidators, AuthUserValidators):
    def __init__(self):
        super(APIKeysValidators, self).__init__()

    def organization_exist(self, organization_id: typing.Union[str, None]) -> bool:
        does_organization_exist: typing.Union[bool, None] = self.is_organization_exist(organization_id=organization_id)
        if isinstance(does_organization_exist, bool):
            return does_organization_exist
        raise DataServiceError(status=500, description="Database Error: Unable to verify organization")

    def user_can_create_key(self, uid: typing.Union[str, None], organization_id: typing.Union[str, None]) -> bool:
        is_member_of_org: typing.Union[bool, None] = self.user_is_member_of_org(uid=uid, organization_id=organization_id)
        user_is_admin: typing.Union[bool, None] = self.org_user_is_admin(uid=uid, organization_id=organization_id)
        if isinstance(is_member_of_org, bool) and isinstance(user_is_admin, bool):
            return is_member_of_org and user_is_admin
        raise DataServiceError(status=500, description="Database Error: Unable to verify user")


class APIKeysView(APIKeysValidators):
    def __init__(self):
        super(APIKeysView, self).__init__()

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

                :param domain:
                :param uid:
                :param organization_id:
            :return:
        ***REMOVED***
        org_exist = self.organization_exist(organization_id=organization_id)
        can_create_key = self.user_can_create_key(uid=uid, organization_id=organization_id)
        if org_exist and can_create_key:
            # create key secret key combo
            api_key: str = create_id()
            secret_token: str = create_id()
            api_key_instance: APIKeys = APIKeys(organization_id=organization_id,
                                                api_key=api_key,
                                                secret_token=secret_token,
                                                assigned_to_uid=uid,
                                                domain=domain,
                                                is_active=True)
            key = api_key_instance.put()
            if key is None:
                message: str = "database error: unable to create api_key"
                raise DataServiceError(status=500, description=message)
            message: str = "successfully created api_key secret_token combo"
            return jsonify({'status': True, 'payload': api_key_instance.to_dict(),
                            'message': message}), 200
        return jsonify({'status': False, 'message': 'User not authorized to create keys'}), 500

    @use_context
    @handle_view_errors
    def deactivate_key(self, key: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            admin only function
        :param key:
        :return:
        ***REMOVED***

        api_key_instance: APIKeys = APIKeys.query(APIKeys.key == key).get()
        if isinstance(api_key_instance, APIKeys):
            api_key_instance.is_active = False
            key = api_key_instance.put()
            if key is None:
                message: str = "database error: unable to deactivate_key"
                raise DataServiceError(status=500, description=message)
            message: str = "successfully deactivated api_key"
            return jsonify({'status': True, 'payload': api_key_instance.to_dict(),
                            'message': message}), 200
        return jsonify({'status': False, 'message': 'api key not found'}), 500

    @use_context
    @handle_view_errors
    def activate_key(self, key: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            admin only function
        :param key:
        :return:
        ***REMOVED***

        api_key_instance: APIKeys = APIKeys.query(APIKeys.key == key).get()
        if isinstance(api_key_instance, APIKeys):
            api_key_instance.is_active = True
            key = api_key_instance.put()
            if key is None:
                message: str = "database error: unable to activate_key"
                raise DataServiceError(status=500, description=message)
            message: str = "successfully activated api_key"
            return jsonify({'status': True, 'payload': api_key_instance.to_dict(),
                            'message': message}), 200
        return jsonify({'status': False, 'message': 'api key not found'}), 500

    @cache_affiliates.cached(timeout=return_ttl(name='short'))
    @use_context
    @handle_view_errors
    def return_organization_keys(self, organization_id: typing.Union[str, None]) -> tuple:

        api_keys_list: typing.List[APIKeys] = APIKeys.query(APIKeys.organization_id == organization_id).fetch()
        payload: typing.List[dict] = [_key.to_dict() for _key in api_keys_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'organization keys returned successfully'}), 200

