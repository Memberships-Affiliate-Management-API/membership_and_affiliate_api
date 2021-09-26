"""
    **Module - View Controller for Affiliates API**
    *Class Definitions for managing access to the database and validation of user input*

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from email import message
from typing import Optional, List

import self as self
from flask import current_app, jsonify
from google.cloud import ndb

from _sdk._email import Mailgun
from cache.cache_manager import app_cache
from config.exception_handlers import handle_view_errors
from config.exceptions import DataServiceError, InputError, UnAuthenticatedError, error_codes, status_codes
from config.use_context import use_context
from database.affiliates import Affiliates, Recruits, EarningsData
from database.affiliates import AffiliatesValidators as ValidAffiliate
from database.affiliates import EarningsValidators as ValidEarnings
from database.affiliates import RecruitsValidators as ValidRecruit
from utils.utils import create_id, return_ttl


# from cache.cache_manager import CacheManager


class AffiliatesEmails(Mailgun):
    """
        **Class AffiliatesEmails**
            gives the ability to send email notifications to affiliates when certain
            actions must be taken or updates have occurred.

        **Class Methods**
            1. __do_send_mail -> actually send emails to users - through mailgun api
    """

    def __init__(self):
        super(AffiliatesEmails, self).__init__()
        self._send_with: str = 'mailgun'
        # TODO add more email providers here


# TODO Create Test Cases for Affiliates View and Documentations
# Dont Edit Just Watch can you see this

class Validator(ValidAffiliate, ValidRecruit, ValidEarnings):
    """
        **Class Validator**
            Gathers validator classes needed for validating actions and input on
            while managing Affiliates.
    """

    def __init__(self):
        super(Validator, self).__init__()

    # noinspection PyTypeChecker
    def can_register_affiliate(self, organization_id: str, uid: str) -> bool:
        """
            **can_register_affiliate**
                returns true if user can add an affiliate into this organization
        :param organization_id:
        :param uid:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = "organization_id is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(uid, str) or not bool(uid.strip()):
            message: str = "uid is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        # this means the user recruiting this affiliate is already a registered affiliate
        already_registered: typing.Union[bool, None] = self.recruiter_registered(organization_id=organization_id,
                                                                                 uid=uid)
        if isinstance(already_registered, bool):
            return not already_registered
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(status=error_codes.data_service_error_code, description=message)

    def _create_unique_affiliate_id(self) -> str:
        """
            **_create_unique_affiliate_id**
                returns an id that does not conflict with any affiliate id
        :return:
        """
        _id = create_id()
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == _id).get()
        return self._create_unique_affiliate_id() if affiliate_instance.uid == _id else _id


# noinspection DuplicatedCode
class AffiliatesView(Validator):
    """
        **Class AffiliatesView**
            Enables the api to access methods to access data and create and update affiliates
            also insures that input is validated and users are authenticated

    """

    def __init__(self):
        super(AffiliatesView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def register_affiliate(self, affiliate_data: dict) -> tuple:
        """
            **register_affiliate**
                Register new affiliate, affiliate_data must contain the uid of the affiliate
                being recruited and organization_id of the organization recruiting the affiliate.

        :param affiliate_data:
        :return: tuple with registered affiliate
        """
        uid: Optional[str] = affiliate_data.get('uid')
        organization_id: Optional[str] = affiliate_data.get('organization_id')
        # NOTE can register affiliate will check organization_id and uid are valid
        if not self.can_register_affiliate(organization_id=organization_id, uid=uid):
            message: str = "You are not authorized to register as an affiliate"
            raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)
        # NOTE: this creates globally unique Affiliate Key
        affiliate_id: str = self._create_unique_affiliate_id()
        # NOTE: other affiliates fields will be auto completed - be defaults

        affiliate_instance: Affiliates = Affiliates(**affiliate_data)

        key: Optional[ndb.Key] = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            message: str = "There was an error creating Affiliate"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        print('affiliate instance: ', affiliate_instance)
        # scheduling cache deletions
        _kwargs: dict = dict(affiliates_view=self, organization_id=organization_id, affiliate_id=affiliate_id)
        app_cache._schedule_cache_deletion(func=app_cache._delete_affiliate_cache, kwargs=_kwargs)

        return jsonify({'status': True,
                        'message': 'successfully registered an affiliate',
                        'payload': affiliate_instance.to_dict()}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def total_recruits(self, affiliate_data: dict, add: int = 0) -> tuple:
        """
            **total_recruits**
            given an existing affiliate update total recruits field in the affiliate record

        :param affiliate_data:
        :param add:
        :return:
        """
        affiliate_id: Optional[str] = affiliate_data.get('affiliate_id')
        organization_id: Optional[str] = affiliate_data.get('organization_id')

        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(add, int):
            message: str = "add: amount to update total_recruits is required"
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.affiliate_id == affiliate_id).get()

        if bool(affiliate_instance) and affiliate_instance.affiliate_id == affiliate_id:
            affiliate_instance.total_recruits += add
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "Something went wrong while updating affiliate"
                raise DataServiceError(status=500, description=message)

            # deleting affiliate Caches related to the updated record
            _kwargs: dict = dict(affiliates_view=AffiliatesView, organization_id=organization_id,
                                 affiliate_id=affiliate_id)

            app_cache._schedule_cache_deletion(func=app_cache._delete_affiliate_cache, kwargs=_kwargs)

            return jsonify({'status': True,
                            'message': 'successfully incremented total recruits',
                            'payload': affiliate_instance.to_dict()}), status_codes.successfully_updated_code
        else:
            return jsonify({'status': False, 'message': 'Failed to locate affiliate'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def delete_affiliate(self, affiliate_data: dict) -> tuple:
        """
            **delete_affiliate**
                the function soft delete an affiliate record.

                affiliate_id: is the id of the affiliate to be marked as deletedItem
                organization_id: is the id of the organization from which the affiliate is to be deleted

            :param affiliate_data: dict containing affiliate_id and organization_id
            :return: tuple containing the record of the deleted affiliate
        """

        affiliate_id: Optional[str] = affiliate_data.get('affiliate_id')
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = affiliate_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        # TODO - need to add verifications only admin and owner of account can delete affiliate

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.affiliate_id == affiliate_id).get()
        if bool(affiliate_instance) and affiliate_instance.affiliate_id == affiliate_id:
            affiliate_instance.is_active = False
            affiliate_instance.is_deleted = True
            key: Optional[ndb.Key] = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = 'something went wrong while deleting affiliate'
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # scheduling affiliate cache deletions
            _kwargs: dict = dict(affiliates_view=AffiliatesView, organization_id=organization_id,
                                 affiliate_id=affiliate_id)
            app_cache._schedule_cache_deletion(func=app_cache._delete_affiliate_cache, kwargs=_kwargs)

            return jsonify({'status': True,
                            'message': 'successfully deleted the affiliate',
                            'payload': affiliate_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = "Affiliate not found: delete operation cannot be completed"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def mark_active(self, affiliate_data: dict, is_active: bool) -> tuple:
        """
            **mark_active**
                affiliate_id of the affiliate to be marked as active.
                this action will not have an effect if the affiliate has been soft-deleted

        :param affiliate_data: contains affiliate_id and organization_id
        :param is_active:
        :return:
        """
        affiliate_id: Optional[str] = affiliate_data.get('affiliate_id')
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = affiliate_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(is_active, bool):
            raise ValueError("is_active is required and can only be a boolean")

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.affiliate_id == affiliate_id).get()

        if bool(affiliate_instance) and affiliate_instance.affiliate_id == affiliate_id:
            if affiliate_instance.is_deleted and is_active:
                message: str = "cannot activate / de-activate an affiliate if the affiliate has been deleted"
                raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

            affiliate_instance.is_active = is_active
            key: Optional[ndb.Key] = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "An Unknown Error occurred while trying to mark affiliate as in-active"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # scheduling affiliate cache deletion
            _kwargs: dict = dict(affiliates_view=AffiliatesView, organization_id=organization_id,
                                 affiliate_id=affiliate_id)
            app_cache._schedule_cache_deletion(func=app_cache._delete_affiliate_cache, kwargs=_kwargs)

            return jsonify({'status': True, 'message': 'successfully marked affiliate as inactive',
                            'payload': affiliate_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = "Affiliate Not Found: Unable to update record"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_affiliate(self, affiliate_data: dict) -> tuple:
        """
            **get_affiliate**
                obtains a record of one affiliate from the store. given either uid or affiliate_id, organization_id
                must be valid

        :param affiliate_data: contains affiliate_id and organization_id the affiliate must belong to the organization
        :return: response contain affiliate record
        """
        organization_id: Optional[str] = affiliate_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliate_id: Optional[str] = affiliate_data.get('affiliate_id')

        # Initializing affiliate_instance to None in order to allow testing for valid data
        affiliate_instance: Optional[Affiliates] = None
        valid_input: bool = False
        # NOTE this means if affiliate_id is valid
        if isinstance(affiliate_id, str) and bool(affiliate_id.strip()):
            valid_input = True
            affiliate_instance = Affiliates.query(Affiliates.organization_id == organization_id,
                                                  Affiliates.affiliate_id == affiliate_id).get()

        uid: Optional[str] = affiliate_data.get('uid')
        if isinstance(uid, str) and bool(uid.strip()):
            valid_input = True
            affiliate_instance = Affiliates.query(Affiliates.organization_id == organization_id,
                                                  Affiliates.uid == uid).get()

        # if we are here and still dont have a valid input set to true then we have a problem with input data
        if not valid_input:
            message: str = "affiliate_id or uid is required to get affiliate record"
            raise InputError(status=error_codes.input_error_code, description=message)

        # Note checking if we have valid data and then return to user
        if bool(affiliate_instance) and affiliate_instance.uid == uid:
            return jsonify({'status': True,
                            'message': 'successfully obtained affiliate data',
                            'payload': affiliate_instance.to_dict()}), status_codes.status_ok_code

        message: str = 'Affiliate Not Found: unable to locate affiliate'
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_all_affiliates(self, organization_id: Optional[str]) -> tuple:
        """
            **get_all_affiliates**
                returns a list of all affiliates that belongs to the organization

            :param organization_id: the organization id to return affiliates off
            :return: response containing the list of affiliates as payload
            status code ${status_codes.status_ok_code}
        """

        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliates_list: List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id).order(Affiliates.datetime_recruited).fetch()
        # TODO use Generators to get affiliates in a batch of thousand at a time
        payload: List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]

        if len(payload):
            message: str = "Successfully returned all affiliates"
            return jsonify({'status': True,
                            'message': message,
                            'payload': payload}), status_codes.status_ok_code

        message: str = "There are no affiliate records in this organization"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_active_affiliates(self, organization_id: Optional[str]) -> tuple:
        """
            **get_active_affiliates**
                NOTE: active affiliates but not deleted
                returns a list of active affiliates in an organization

        :param organization_id: the organization id of the organization to return the affiliates
        :return: response containing the list of active affiliates
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliates_list: List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id,
            Affiliates.is_active == True, Affiliates.is_deleted == False).order(Affiliates.datetime_recruited).fetch()

        # TODO use Generators to get affiliates in a batch of thousand at a time
        payload: List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        if len(payload):
            return jsonify({'status': True, 'message': 'successfully returned all affiliates',
                            'payload': payload}), status_codes.status_ok_code

        # Note failed to find active affiliates
        message: str = "Unable to find active affiliates"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_in_active_affiliates(self, organization_id: Optional[str]) -> tuple:
        """
            **get_in_active_affiliates**
                returns a list of affiliates who are not active - but not deleted

        :param organization_id: the organization_id of the organization to return affiliates of
        :return: a response tuple with a payload of in-active affiliates from the organization
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliates_list: List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id, Affiliates.is_active == False,
            Affiliates.is_deleted == False).order(Affiliates.datetime_recruited).fetch()

        payload: List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        if len(payload):
            message: str = "successfully returned all affiliates"
            return jsonify({'status': True,
                            'message': message,
                            'payload': payload}), status_codes.status_ok_code

        message: str = "Unable to find affiliates who are in-active"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_deleted_affiliates(self, organization_id: Optional[str]) -> tuple:
        """
            **get_deleted_affiliates**
                return deleted affiliates by organization_id

        :param organization_id:
        :return: response containing the list of affiliates who are deleted
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliates_list: List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id,
            Affiliates.is_deleted == True).order(Affiliates.datetime_recruited).fetch()

        payload: List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        if len(payload):
            message: str = "Successfully returned deleted affiliates"
            return jsonify({'status': True,
                            'message': message,
                            'payload': payload}), status_codes.status_ok_code
        message: str = "Unable to find deleted affiliates"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_not_deleted_affiliates(self, organization_id: Optional[str]) -> tuple:
        """
            **get_not_deleted_affiliates**
                # NOTE: this function may be redundant
                returns a list of affiliates which are not deleted by  ORGANIZATION_ID
        :param : organization_id: the organization to return deleted affiliates from
        :return : response containing the list of deleted affiliates
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliates_list: List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id,
            Affiliates.is_deleted == False).order(Affiliates.datetime_recruited).fetch()

        payload: List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        if len(payload):
            message: str = "Successfully returned affiliates which are not deleted"
            return jsonify({'status': True,
                            'message': message,
                            'payload': payload}), status_codes.status_ok_code

        message: str = "Unable to locate not deleted affiliates"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code


# noinspection DuplicatedCode
class RecruitsView(Validator):
    """
        View Manager for Recruits
        Used by affiliates to register newly recruited members
    """

    def __init__(self):
        super(RecruitsView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    # TODO validate Recruits

    @use_context
    @handle_view_errors
    def add_recruit(self, recruit_data: dict) -> tuple:
        """
            given referrer_uid , and organization_id, add new recruit
        :param recruit_data:
        :return:
        """
        # TODO - the action of creating a recruit also modifies the affiliate record who is recruiting
        #  this means an update is also needed on the relevant affiliate record

        referrer_uid: Optional[str] = recruit_data.get('referrer_uid')
        if not isinstance(referrer_uid, str) or not bool(referrer_uid.strip()):
            message: str = 'referrer_uid is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = recruit_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        affiliate_id = self._create_unique_affiliate_id()
        recruit_instance: Recruits = Recruits(**recruit_data, affiliate_id=affiliate_id)

        key = recruit_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not bool(key):
            message: str = "An Error occurred while adding new recruit"
            raise DataServiceError(status=error_codes.data_service_error_code, description=message)

        # NOTE scheduling recruits cache deleter
        _kwargs: dict = dict(recruits_view=RecruitsView, organization_id=organization_id,
                             is_active=recruit_instance.is_active, is_deleted=recruit_instance.is_deleted,
                             affiliate_data=None, recruit_data=recruit_data)
        app_cache._schedule_cache_deletion(func=app_cache._delete_recruits_cache, kwargs=_kwargs)

        return jsonify({'status': True, 'message': 'Successfully created new recruit',
                        'payload': recruit_instance.to_dict()}), status_codes.successfully_updated_code

    @use_context
    @handle_view_errors
    def delete_recruit(self, recruit_data: dict) -> tuple:
        """
            affiliate_id: is the id of the recruit, of which the record must be removed as a recruit

        :param recruit_data:
        :return: tuple as response
        """
        # TODO - the action of deleting a recruit also modifies the affiliate record who is recruiting
        #  this means an update is also needed on the relevant affiliate record

        # Note: affiliate_id of the recruit
        affiliate_id: Optional[str] = recruit_data.get('affiliate_id')
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = recruit_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        recruit_instance: Recruits = Recruits.query(Recruits.organization_id == organization_id,
                                                    Recruits.affiliate_id == affiliate_id).get()

        if bool(recruit_instance) and recruit_instance.affiliate_id == affiliate_id:
            # Soft Deleting Recruit
            recruit_instance.is_deleted = True
            recruit_instance.is_active = False
            # TODO- update stats and organization Class - Consider doing this from an API
            key = recruit_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "An Error occurred while deleting recruit"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # Note: scheduling recruits cache deletions
            _kwargs: dict = dict(recruits_view=RecruitsView, organization_id=organization_id,
                                 is_active=recruit_instance.is_active, is_deleted=recruit_instance.is_deleted,
                                 affiliate_data=None, recruit_data=recruit_data)

            app_cache._schedule_cache_deletion(func=app_cache._delete_recruits_cache, kwargs=_kwargs)

            return jsonify({'status': True, 'message': 'Successfully deleted recruit',
                            'payload': recruit_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = "Recruit does not exist: Cannot Delete"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def mark_active(self, recruit_data: dict, is_active: bool) -> tuple:
        """
            convert a recruit into an active or inactive recruit
        :param recruit_data:
        :param is_active:
        :return:
        """
        affiliate_id: Optional[str] = recruit_data.get('affiliate_id')
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = recruit_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not isinstance(is_active, bool):
            message: str = 'is_active is required and can only be a boolean'
            raise InputError(status=error_codes.input_error_code, description=message)

        recruit_instance: Recruits = Recruits.query(Recruits.organization_id == organization_id,
                                                    Recruits.affiliate_id == affiliate_id).get()

        if bool(recruit_instance) and recruit_instance.affiliate_id == affiliate_id:
            recruit_instance.is_active = is_active
            key = recruit_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not bool(key):
                message: str = "An Error occurred while changing recruit active status"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            _kwargs: dict = dict(recruits_view=RecruitsView, organization_id=organization_id,
                                 is_active=is_active, is_deleted=recruit_instance.is_deleted,
                                 affiliate_data=None, recruit_data=recruit_data)

            app_cache._schedule_cache_deletion(func=app_cache._delete_recruits_cache, kwargs=_kwargs)

            return jsonify({'status': True, 'message': 'Successfully deleted recruit',
                            'payload': recruit_instance.to_dict()}), status_codes.successfully_updated_code

        message: str = "Recruit does not exist"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_recruit(self, recruit_data: dict) -> tuple:
        """
            given affiliate_id return recruit organization_id has to be valid
        :param recruit_data:
        :return:
        """
        affiliate_id: Optional[str] = recruit_data.get('affiliate_id')
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = recruit_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        recruit_instance: Recruits = Recruits.query(Recruits.organization_id == organization_id,
                                                    Recruits.affiliate_id == affiliate_id).get()

        if bool(recruit_instance) and recruit_instance.affiliate_id == affiliate_id:
            message: str = "Successfully retrieved recruit"
            return jsonify({'status': True,
                            'payload': recruit_instance.to_dict(),
                            'message': message}), status_codes.successfully_updated_code

        message: str = "Recruit does not exist"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_recruits_by_active_status(self, organization_id: str, is_active: bool) -> tuple:
        """
            get recruit by active status
        :param organization_id:
        :param is_active:
        :return:
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not (isinstance(is_active, bool)):
            message: str = 'is_active status is required and its boolean'
            raise InputError(status=error_codes.input_error_code, description=message)

        recruits_list: List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                       Recruits.is_active == is_active).fetch()

        payload: List[dict] = [recruit.to_dict() for recruit in recruits_list]
        message: str = "{} recruits successfully fetched recruits by active status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), status_codes.status_ok_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_recruits_by_deleted_status(self, organization_id: str, is_deleted: bool) -> tuple:
        """
            **get_recruits_by_deleted_status**
                returns recruits matching deleted status when true returns deleted when
                false returns recruits which are not deleted

        :param organization_id: str -> the organization_id for the organization to search recruits
        :param is_deleted: bool -> True if you want to search for deleted recruits
        :return: tuple -> response, status_codes , response contains results of the search in payload
        """
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not (isinstance(is_deleted, bool)):
            message: str = 'is_deleted status is required and is boolean'
            raise InputError(status=error_codes.input_error_code, description=message)

        recruits_list: List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                       Recruits.is_deleted == is_deleted).fetch()

        payload = [recruit.to_dict() for recruit in recruits_list]
        message: str = "{} recruits successfully fetched recruits by deleted status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), status_codes.status_ok_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_recruits_by_affiliate(self, affiliate_data: dict) -> tuple:
        """
            **get_recruits_by_affiliate**
                return recruits belonging to a certain affiliate

        :param affiliate_data:
        :return: list of recruits belonging to a specific affiliate
        """

        affiliate_id: Optional[str] = affiliate_data.get('affiliate_id')
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = affiliate_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        recruits_list: List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                       Recruits.affiliate_id == affiliate_id).fetch()

        payload: List[dict] = [recruit.to_dict() for recruit in recruits_list]
        if len(payload):
            message: str = "{} recruits successfully fetched recruits by active status".format(str(len(recruits_list)))
            return jsonify({'status': True, 'message': message, 'payload': payload}), status_codes.status_ok_code

        message: str = "affiliate recruits not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def get_recruits_by_active_affiliate(self, affiliate_data: dict, is_active: bool) -> tuple:
        """
            # TODO this function may be irrelevant further refining is needed here
            return a list of recruits by is_active status
        :param affiliate_data:
        :param is_active:
        :return:
        """
        affiliate_id: Optional[str] = affiliate_data.get('affiliate_id')
        if not isinstance(affiliate_id, str) or not bool(affiliate_id.strip()):
            message: str = 'affiliate_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        organization_id: Optional[str] = affiliate_data.get('organization_id')
        if not isinstance(organization_id, str) or not bool(organization_id.strip()):
            message: str = 'organization_id is required'
            raise InputError(status=error_codes.input_error_code, description=message)

        if not (isinstance(is_active, bool)):
            message: str = 'is_active status is required and can only be a boolean'
            raise InputError(status=error_codes.input_error_code, description=message)

        recruits_list: List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                       Recruits.affiliate_id == affiliate_id,
                                                       Recruits.is_active == is_active).fetch()

        payload: List[dict] = [recruit.to_dict() for recruit in recruits_list]
        if len(payload):
            message: str = "{} recruits successfully fetched affiliate recruits by status".format(
                str(len(recruits_list)))
            return jsonify({'status': True, 'message': message, 'payload': payload}), status_codes.status_ok_code

        message: str = "recruits by is_active status not found"
        return jsonify({'status': False, 'message': message}), status_codes.data_not_found_code


class EarningsView(Validator):
    """
        Used by system to register new earnings for affiliates
        # TODO finalize the Earnings Class
    """

    def __init__(self):
        super(EarningsView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def register_earnings(self, earnings_data: dict) -> tuple:
        """
        **register_earnings**
            register new earnings record
        """
        # TODO verify input data
        earnings_instance: EarningsData = EarningsData(**earnings_data)
        key: Optional[ndb.Key] = earnings_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if not isinstance(key, ndb.Key):
            _message: str = 'Database Error: creating new earnings record'
            raise DataServiceError(status=error_codes.data_service_error_code, description=_message)

        _message: str = 'successfully created new earnings record'
        return jsonify(dict(status=True,
                            payload=earnings_instance.to_dict(),
                            message=_message)), status_codes.successfully_updated_code

    def mark_paid(self, earnings_data: dict, is_paid: bool) -> tuple:
        """
            mark earnings record as paid or not paid
        """
        if not isinstance(is_paid, bool):
            _message: str = 'is_paid is required and should be boolean'
            raise InputError(status=error_codes.input_error_code, description=_message)

        earnings_instance: EarningsData = EarningsData.query(
            EarningsData.affiliate_id == earnings_data.get('affiliate_id'),
            EarningsData.organization_id == earnings_data.get('organization_id')).get()
        if isinstance(earnings_instance, EarningsData) and bool(earnings_instance):
            earnings_instance.is_paid = is_paid
            key: Optional[ndb.Key] = earnings_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not isinstance(key, ndb.Key):
                _message: str = 'Database Error: updating earnings record'
                raise DataServiceError(status=error_codes.data_service_error_code, description=_message)

            _message: str = 'successfully updated earnings data'
            return jsonify(dict(status=True,
                                payload=earnings_instance.to_dict(),
                                message=_message)), status_codes.successfully_updated_code

    def mark_on_hold(self, earnings_data: dict, on_hold: bool) -> tuple:
        """
            mark earnings as on hold or not on hold
            earnings which are on-hold may not be paid until problem is resolved
        """
        if not isinstance(on_hold, bool):
            _message: str = 'on_hold is required and can only be a boolean'
            raise InputError(status=error_codes.input_error_code, description=_message)

        affiliate_id: Optional[str] = earnings_data.get('affiliate_id')
        organization_id: Optional[str] = earnings_data.get('organization_id')

        earnings_instance: EarningsData = EarningsData.query(EarningsData.affiliate_id == affiliate_id,
                                                             EarningsData.organization_id == organization_id).get()

        if isinstance(earnings_instance, EarningsData) and bool(earnings_instance):
            earnings_instance.on_hold = on_hold
            key: Optional[ndb.Key] = earnings_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if not isinstance(key, ndb.Key):
                _message: str = 'Database Error: updating earnings data'
                raise DataServiceError(status=error_codes.data_service_error_code, description=_message)
            _message: str = 'successfully updated earnings data'
            return jsonify(dict(status=True, payload=earnings_instance.to_dict(),
                                message=_message)), status_codes.successfully_updated_code


    def transfer_earnings_to_wallet(self, earnings_data: dict) -> tuple:
        """
            transfer earnings to wallet
            wallet earnings can be sent to paypal or through EFT
        """
        pass
