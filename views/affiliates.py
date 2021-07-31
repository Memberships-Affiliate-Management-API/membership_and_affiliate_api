import typing
from flask import current_app, jsonify
from main import app_cache
from database.affiliates import AffiliatesValidators as ValidAffiliate
from database.affiliates import RecruitsValidators as ValidRecruit
from database.affiliates import EarningsValidators as ValidEarnings
from database.affiliates import Affiliates, Recruits
from config.exceptions import DataServiceError
from utils.utils import create_id, return_ttl, end_of_month, can_cache
from config.exception_handlers import handle_view_errors
from config.use_context import use_context


# TODO Create Test Cases for Affiliates View and Documentations
# Dont Edit Just Watch can you see this

class Validator(ValidAffiliate, ValidRecruit, ValidEarnings):
    ***REMOVED***
        Affiliates View Validators,
    ***REMOVED***

    def __init__(self):
        super(Validator, self).__init__()

    # noinspection PyTypeChecker
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def can_register_affiliate(self, organization_id: str, uid: str) -> bool:
        already_registered: typing.Union[bool, None] = self.user_already_registered(
            organization_id=organization_id, uid=uid)
        if not isinstance(already_registered, bool):
            raise ValueError("invalid user id")
        print("User Already Registered: {}".format(already_registered))
        return not already_registered


# noinspection DuplicatedCode
class AffiliatesView(Validator):
    ***REMOVED***
        Register new affiliates using this class
    ***REMOVED***

    def __init__(self):
        super(AffiliatesView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def register_affiliate(self, affiliate_data: dict) -> tuple:
        ***REMOVED***
            Register new affiliate, affiliate_data must contain the uid of the affiliate
            being recruited and organization_id of the organization recruiting the affiliate.

        ***REMOVED***
        uid: typing.Union[None, str] = affiliate_data.get('uid')
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')

        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'user id cannot be Null'}), 500
        if self.can_register_affiliate(organization_id=organization_id, uid=uid) is True:
            affiliate_instance: Affiliates = Affiliates(organization_id=organization_id, affiliate_id=create_id(),
                                                        uid=uid)
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "There was an error creating Affiliate"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True,
                            'message': 'successfully registered an affiliate',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'User already registered as an Affiliate'}), 500

    @use_context
    @handle_view_errors
    def total_recruits(self, affiliate_data: dict, add: int = 0) -> tuple:
        ***REMOVED***
            update an existing affiliate
        ***REMOVED***
        affiliate_id: typing.Union[str, None] = affiliate_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.affiliate_id == affiliate_id).get()

        if isinstance(affiliate_instance, Affiliates):
            affiliate_instance.total_recruits += add
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "Something went wrong while updating affiliate"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True,
                            'message': 'successfully incremented total recruits',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'Failed to locate affiliate'}), 500

    @use_context
    @handle_view_errors
    def delete_affiliate(self, affiliate_data: dict) -> tuple:
        ***REMOVED***
            the function soft delete an affiliate record.

            affiliate_id: is the id of the affiliate to be marked as deletedItem
            organization_id: is the id of the organization from which the affiliate is to be deleted

            :param affiliate_data: dict containing affiliate_id and organization_id
            :return: tuple containing the record of the deleted affiliate
        ***REMOVED***

        affiliate_id: typing.Union[None, str] = affiliate_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.affiliate_id == affiliate_id).get()
        if isinstance(affiliate_instance, Affiliates):
            affiliate_instance.is_active = False
            affiliate_instance.is_deleted = True
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = 'something went wrong while deleting affiliate'
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True,
                            'message': 'successfully deleted the affiliate',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'error locating that affiliate'}), 500

    @use_context
    @handle_view_errors
    def mark_active(self, affiliate_data: dict, is_active: bool) -> tuple:
        ***REMOVED***
            affiliate_id of the affiliate to be marked as active.
            this action will not have an effect if the affiliate has been soft-deleted
        :param affiliate_data: contains affiliate_id and organization_id
        :param is_active:
        :return:
        ***REMOVED***

        affiliate_id: typing.Union[None, str] = affiliate_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500
        if not isinstance(is_active, bool):
            raise ValueError("is_active is required and can only be a boolean")

        affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                          Affiliates.affiliate_id == affiliate_id).get()

        if isinstance(affiliate_instance, Affiliates):
            if affiliate_instance.is_deleted and is_active:
                message: str = "cannot activate an affiliate if the affiliate has been deleted"
                return jsonify({'status': False, 'message': message}), 200

            affiliate_instance.is_active = is_active
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Unknown Error occurred while trying to mark affiliate as in-active"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'message': 'successfully marked affiliate as inactive',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            message: str = "Unable to locate affiliate record"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_affiliate(self, affiliate_data: dict) -> tuple:
        ***REMOVED***
            obtains a record of one affiliate from the store.
        :param affiliate_data: contains affiliate_id and organization_id the affiliate must belong to the organization
        :return: response contain affiliate record
        ***REMOVED***
        affiliate_id: typing.Union[None, str] = affiliate_data.get('affiliate_id')
        uid: typing.Union[None, str] = affiliate_data.get('uid')
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')

        if (uid is None) and (affiliate_id is None):
            return jsonify({'status': False, 'message': 'uid or affiliate_id is required to fetch affiliate'}), 500
        if uid is not None:
            affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                              Affiliates.uid == uid).get()
        else:
            affiliate_instance: Affiliates = Affiliates.query(Affiliates.organization_id == organization_id,
                                                              Affiliates.affiliate_id == affiliate_id).get()

        if isinstance(affiliate_instance, Affiliates):
            return jsonify({'status': True,
                            'message': 'successfully obtained affiliate data',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'unable to locate affiliate'}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_all_affiliates(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            returns a list of all affiliates that belongs to the organization
            :param organization_id: the organization id to return affiliates off
            :return: response containing the list of affiliates as payload
        ***REMOVED***
        affiliates_list: typing.List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id).fetch()
        payload: typing.List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        message: str = "Successfully returned all affiliates"
        return jsonify({'status': True,
                        'message': message,
                        'payload': payload}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_active_affiliates(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return affiliates who are not deleted and are active
        ***REMOVED***
        affiliates_list: typing.List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id,
            Affiliates.is_active == True, Affiliates.is_deleted == False).fetch()
        payload: typing.List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        return jsonify({'status': True, 'message': 'successfully returned all affiliates',
                        'payload': payload}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_in_active_affiliates(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return affiliates who are not active
        ***REMOVED***
        affiliates_list: typing.List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id, Affiliates.is_active == False,
            Affiliates.is_deleted == False).fetch()

        payload: typing.List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        message: str = "successfully returned all affiliates"
        return jsonify({'status': True,
                        'message': message,
                        'payload': payload}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_deleted_affiliates(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return affiliates who are not active
        ***REMOVED***
        affiliates_list: typing.List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id,
            Affiliates.is_deleted == True).fetch()
        payload: typing.List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        message: str = "Successfully returned deleted affiliates"
        return jsonify({'status': True,
                        'message': message,
                        'payload': payload}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_not_deleted_affiliates(self, organization_id: typing.Union[str, None]) -> tuple:
        ***REMOVED***
            return affiliates who are not active
        ***REMOVED***
        affiliates_list: typing.List[Affiliates] = Affiliates.query(
            Affiliates.organization_id == organization_id,
            Affiliates.is_deleted == False).fetch()

        payload: typing.List[dict] = [affiliate.to_dict() for affiliate in affiliates_list]
        message: str = "Successfully returned affiliates which are not deleted"
        return jsonify({'status': True,
                        'message': message,
                        'payload': payload}), 200


# noinspection DuplicatedCode
class RecruitsView(Validator):
    ***REMOVED***
        Used by affiliates to register newly recruited members
    ***REMOVED***

    def __init__(self):
        super(RecruitsView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    # TODO validate Recruits

    @use_context
    @handle_view_errors
    def add_recruit(self, recruit_data: dict) -> tuple:
        ***REMOVED***
            recruit_data: dict
        ***REMOVED***
        referrer_uid: typing.Union[None, str] = recruit_data.get('referrer_uid')
        organization_id: typing.Union[str, None] = recruit_data.get('organization_id')

        if (referrer_uid is None) or (referrer_uid == ""):
            return jsonify({'status': False, 'message': 'referrer uid is required'}), 200

        recruit_instance: Recruits = Recruits(organization_id=organization_id, affiliate_id=create_id(), referrer_uid=referrer_uid)
        key = recruit_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if key is None:
            message: str = "An Error occurred while adding new recruit"
            raise DataServiceError(status=500, description=message)
        return jsonify({'status': True, 'message': 'Successfully created new recruit',
                        'payload': recruit_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    def delete_recruit(self, recruit_data: dict) -> tuple:
        ***REMOVED***
            affiliate_id: is the id of the recruit, of which the record must be removed as a recruit

        :param recruit_data:
        :return: tuple as response
        ***REMOVED***
        # Note: affiliate_id of the recruit
        affiliate_id: typing.Union[str, None] = recruit_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = recruit_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                              Recruits.affiliate_id == affiliate_id).fetch()

        if isinstance(recruits_list, list) and len(recruits_list) > 0:
            recruits_instance = recruits_list[0]
            # Soft Deleting Recruit
            recruits_instance.is_deleted = True
            recruits_instance.is_active = False
            # TODO- update stats and organization Class - Consider doing this from an API
            key = recruits_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Error occurred while deleting recruit"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'message': 'Successfully deleted recruit',
                            'payload': recruits_instance.to_dict()}), 200
        else:
            message: str = "Recruit does not exist"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    def mark_active(self, recruit_data: dict, is_active: bool) -> tuple:
        affiliate_id: typing.Union[str, None] = recruit_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = recruit_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        if not isinstance(is_active, bool):
            return jsonify({'status': False, 'message': 'is_active is required and can only be a boolean'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                              Recruits.affiliate_id == affiliate_id).fetch()

        if isinstance(recruits_list, list) and (len(recruits_list) > 0):
            recruits_instance: Recruits = recruits_list[0]
            recruits_instance.is_active = is_active
            key = recruits_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Error occurred while changing recruit active status"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': True, 'message': 'Successfully deleted recruit',
                            'payload': recruits_instance.to_dict()}), 200
        else:
            message: str = "Recruit does not exist"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_recruit(self, recruit_data: dict) -> tuple:
        affiliate_id: typing.Union[str, None] = recruit_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = recruit_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        recruit_instance: Recruits = Recruits.query(Recruits.organization_id == organization_id,
                                                    Recruits.affiliate_id == affiliate_id).get()

        if isinstance(recruit_instance, Recruits):
            message: str = "Successfully retrieved recruit"
            return jsonify({'status': True, 'payload': recruit_instance.to_dict(), 'message': message}), 200
        else:
            message: str = "Recruit does not exist"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_recruits_by_active_status(self, organization_id: str, is_active: bool) -> tuple:

        if not (isinstance(is_active, bool)):
            return jsonify({'status': False, 'message': 'is_active status is required'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                              Recruits.is_active == is_active).fetch()

        payload: typing.List[dict] = [recruit.to_dict() for recruit in recruits_list]
        message: str = "{} recruits successfully fetched recruits by active status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_recruits_by_deleted_status(self, organization_id: str, is_deleted: bool) -> tuple:

        if not (isinstance(is_deleted, bool)):
            return jsonify({'status': False, 'message': 'is_deleted status is required'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                              Recruits.is_deleted == is_deleted).fetch()

        payload = [recruit.to_dict() for recruit in recruits_list]
        message: str = "{} recruits successfully fetched recruits by deleted status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_recruits_by_affiliate(self, affiliate_data: dict) -> tuple:
        affiliate_id: typing.Union[str, None] = affiliate_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                              Recruits.affiliate_id == affiliate_id).fetch()

        payload: typing.List[dict] = [recruit.to_dict() for recruit in recruits_list]

        message: str = "{} recruits successfully fetched recruits by active status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    @use_context
    @handle_view_errors
    @app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
    def get_recruits_by_active_affiliate(self, affiliate_data: dict, is_active: bool) -> tuple:

        affiliate_id: typing.Union[str, None] = affiliate_data.get('affiliate_id')
        organization_id: typing.Union[str, None] = affiliate_data.get('organization_id')

        if (affiliate_id is None) or (affiliate_id == ""):
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        if not (isinstance(is_active, bool)):
            return jsonify({'status': False, 'message': 'is_active status can only be a boolean'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.organization_id == organization_id,
                                                              Recruits.affiliate_id == affiliate_id,
                                                              Recruits.is_active == is_active).fetch()

        payload: typing.List[dict] = [recruit.to_dict() for recruit in recruits_list]

        message: str = "{} recruits successfully fetched affiliate recruits by status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200


class EarningsView(Validator):
    ***REMOVED***
        Used by system to register new earnings for affiliates
        # TODO finalize the Earnings Class
    ***REMOVED***

    def __init__(self):
        super(EarningsView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def register_earnings(self, earnings_data: dict) -> tuple:
        ***REMOVED***
            register new earnings record
        ***REMOVED***
        pass

    def mark_paid(self, earnings_data: dict, is_paid: bool) -> tuple:
        ***REMOVED***
            mark earnings record as paid or not paid
        ***REMOVED***
        pass

    def mark_on_hold(self, earnings_data: dict, on_hold: bool) -> bool:
        ***REMOVED***
            mark earnings as on hold or not on hold
            earnings which are on-hold may not be paid until problem is resolved
        ***REMOVED***
        pass

    def transfer_earnings_to_wallet(self, earnings_data: dict) -> tuple:
        ***REMOVED***
            transfer earnings to wallet
            wallet earnings can be sent to paypal or through EFT
        ***REMOVED***
        pass
