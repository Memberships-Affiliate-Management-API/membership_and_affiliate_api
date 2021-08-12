***REMOVED***
    **Cache Management Module**

    Classes and methods to manage cache items
***REMOVED***
from main import app_cache
from typing import Optional


class CacheManager:
    ***REMOVED***
        **Class Cache CacheManager**
    ***REMOVED***

    def __init__(self):
        pass

    @staticmethod
    def __delete_user_cache(user_view, organization_id, uid, cell, email) -> bool:
        ***REMOVED***
            **deletes or invalidates invalid user cache
        :param organization_id:
        :param uid:
        :param cell:
        :param email:
        :return:
        ***REMOVED***
        # from views.users import UserView
        # TODO add delete for in-active cache items
        app_cache.delete_memoized(user_view.get_active_users, user_view, organization_id)
        app_cache.delete_memoized(user_view.get_active_users_async, user_view, organization_id)
        app_cache.delete_memoized(user_view.get_all_users, user_view, organization_id)
        app_cache.delete_memoized(user_view.get_all_users_async, user_view, organization_id)
        app_cache.delete_memoized(user_view.get_user, user_view, organization_id, uid, cell, email)
        app_cache.delete_memoized(user_view.get_user_async, user_view, organization_id, uid, cell, email)
        return True

    @staticmethod
    def __delete_organization_cache(org_view, organization_id) -> bool:
        ***REMOVED***
            **__delete_organization_cache**
                deletes or invalidates organization cache items
        :param org_view: OrganizationView Class
        :param organization_id: organization_id
        :return:
        ***REMOVED***
        app_cache.delete_memoized(org_view._return_all_organizations, org_view)
        app_cache.delete_memoized(org_view.get_organization, org_view, organization_id)
        return True

    @staticmethod
    def __delete_wallet_cache(wallet_view, organization_id, uid) -> bool:
        ***REMOVED***
            **__delete_wallet_cache**
                deletes cache items for wallets when a update event occurs on the database
        :param wallet_view:
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        app_cache.delete_memoized(wallet_view.get_wallet, wallet_view, organization_id, uid)
        app_cache.delete_memoized(wallet_view.get_wallet_async, wallet_view, organization_id, uid)
        app_cache.delete_memoized(wallet_view.return_all_wallets, wallet_view, organization_id)
        app_cache.delete_memoized(wallet_view.return_all_wallets_async, wallet_view, organization_id)
        return True

    @staticmethod
    def __delete_membership_cache(membership_view, organization_id, uid, plan_id, status) -> bool:
        ***REMOVED***
            **__delete_membership_cache**
                delete cache items for memberships view

        :param organization_id:
        :param uid:
        :param plan_id:
        :param status:
        :return:
        ***REMOVED***

        return True

    @staticmethod
    def __delete_api_keys_cache(api_keys_view, organization_id) -> bool:
        ***REMOVED***
            **__delete_api_keys_cache**
                delete stale api_keys cache instances
        :return:
        ***REMOVED***
        app_cache.delete_memoized(api_keys_view.return_all_organization_keys, api_keys_view, organization_id)
        app_cache.delete_memoized(api_keys_view.return_active_organization_keys, api_keys_view, organization_id)

        return True

    @staticmethod
    def __delete_affiliate_cache(affiliates_view, organization_id, affiliate_id):
        ***REMOVED***
            **__delete_affiliate_cache**
                deleting affiliate cache on the event that the cache contains outdated data
        :param affiliates_view:
        :param organization_id:
        :param affiliate_id:
        :return:
        ***REMOVED***
        _dict: dict = dict(organization_id=organization_id, affiliate_id=affiliate_id)
        app_cache.delete_memoized(affiliates_view.get_affiliate, affiliates_view, _dict)
        app_cache.delete_memoized(affiliates_view.get_all_affiliates, affiliates_view, organization_id)
        app_cache.delete_memoized(affiliates_view.get_active_affiliates, affiliates_view, organization_id)
        app_cache.delete_memoized(affiliates_view.get_deleted_affiliates, affiliates_view, organization_id)
        app_cache.delete_memoized(affiliates_view.get_not_deleted_affiliates, affiliates_view, organization_id)

    @staticmethod
    def __delete_recruits_cache(recruits_view, organization_id: str, is_active: Optional[bool] = None,
                                is_deleted: Optional[bool] = None, affiliate_data: Optional[dict] = None,
                                recruit_data: Optional[dict] = None) -> bool:
        ***REMOVED***

        :param recruits_view:
        :param organization_id:
        :param is_active:
        :param is_deleted:
        :param affiliate_data:
        :param recruit_data:
        :return:
        ***REMOVED***
        app_cache.delete_memoized(recruits_view.get_recruit, recruits_view, recruit_data)
        app_cache.delete_memoized(recruits_view.get_recruits_by_active_status, recruits_view,
                                  organization_id, is_active)
        app_cache.delete_memoized(recruits_view.get_recruits_by_deleted_status, recruits_view, organization_id,
                                  is_deleted)
        app_cache.delete_memoized(recruits_view.get_recruits_by_affiliate, recruits_view, affiliate_data)
        app_cache.delete_memoized(recruits_view.get_recruits_by_active_affiliate, recruits_view, affiliate_data,
                                  is_active)
        return True
