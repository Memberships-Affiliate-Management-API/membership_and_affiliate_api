***REMOVED***
    **Cache Management Module**
        Classes and methods to manage cache items
        delete cache items which are used in this application
        on view functions
***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from flask_caching import Cache

from datetime import timedelta, datetime
from _cron.scheduler import task_scheduler
from config import config_instance

from typing import Optional, Callable
from utils import datetime_now, create_id


class CacheManager:
    ***REMOVED***
        **Memberships Cache Management**
            utilities to manage cache items for memberships api
    ***REMOVED***

    def __init__(self) -> None:
        self._app_cache: Cache = Cache(config=config_instance.cache_dict())

    def init_app(self, app):
        self.cache.init_app(app=app, config=config_instance.cache_dict())

    @property
    def cache(self) -> Cache:
        return self._app_cache

    @cache.setter
    def cache(self, value: Cache) -> None:
        self._app_cache = value

    def clear_cache(self) -> None:
        ***REMOVED***
        **clear_cache**
            totally clears application cache upon restart

        ***REMOVED***
        self.cache.clear()

    def _delete_user_cache(self, user_view, organization_id, uid, cell, email) -> bool:
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
        self.cache.delete_memoized(user_view.get_active_users, user_view, organization_id)
        self.cache.delete_memoized(user_view.get_active_users_async, user_view, organization_id)
        self.cache.delete_memoized(user_view.get_all_users, user_view, organization_id)
        self.cache.delete_memoized(user_view.get_all_users_async, user_view, organization_id)
        self.cache.delete_memoized(user_view.get_user, user_view, organization_id, uid, cell, email)
        self.cache.delete_memoized(user_view.get_user_async, user_view, organization_id, uid, cell, email)
        return True

    def _delete_organization_cache(self, org_view, organization_id) -> bool:
        ***REMOVED***
            **_delete_organization_cache**
                deletes or invalidates organization cache items
        :param org_view: OrganizationView Class
        :param organization_id: organization_id
        :return:
        ***REMOVED***
        self.cache.delete_memoized(org_view._return_all_organizations, org_view)
        self.cache.delete_memoized(org_view.get_organization, org_view, organization_id)
        return True

    def _delete_wallet_cache(self, wallet_view, organization_id, uid) -> bool:
        ***REMOVED***
            **_delete_wallet_cache**
                deletes cache items for wallets when a update event occurs on the database
        :param wallet_view:
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        self.cache.delete_memoized(wallet_view.get_wallet, wallet_view, organization_id, uid)
        self.cache.delete_memoized(wallet_view.get_wallet_async, wallet_view, organization_id, uid)
        self.cache.delete_memoized(wallet_view.return_all_wallets, wallet_view, organization_id)
        self.cache.delete_memoized(wallet_view.return_all_wallets_async, wallet_view, organization_id)
        return True

    def _delete_membership_cache(self, membership_view, organization_id, uid, plan_id, status) -> bool:
        ***REMOVED***
            **_delete_membership_cache**
                delete cache items for memberships view

        :param organization_id:
        :param uid:
        :param plan_id:
        :param status:
        :return:
        ***REMOVED***
        # TODO- finish this up
        return True

    def _delete_api_keys_cache(self, api_keys_view, api_key, organization_id) -> bool:
        ***REMOVED***
            **_delete_api_keys_cache**
                delete stale api_keys cache instances
        :return:
        ***REMOVED***
        self.cache.delete_memoized(api_keys_view.return_all_organization_keys, api_keys_view, organization_id)
        self.cache.delete_memoized(api_keys_view.return_active_organization_keys, api_keys_view, organization_id)
        self.cache.delete_memoized(api_keys_view.get_api_key, api_keys_view, api_key, organization_id)

        return True

    def _delete_affiliate_cache(self, affiliates_view, organization_id, affiliate_id):
        ***REMOVED***
            **_delete_affiliate_cache**
                deleting affiliate cache on the event that the cache contains outdated data
        :param affiliates_view:
        :param organization_id:
        :param affiliate_id:
        :return:
        ***REMOVED***
        _dict: dict = dict(organization_id=organization_id, affiliate_id=affiliate_id)
        self.cache.delete_memoized(affiliates_view.get_affiliate, affiliates_view, _dict)
        self.cache.delete_memoized(affiliates_view.get_all_affiliates, affiliates_view, organization_id)
        self.cache.delete_memoized(affiliates_view.get_active_affiliates, affiliates_view, organization_id)
        self.cache.delete_memoized(affiliates_view.get_deleted_affiliates, affiliates_view, organization_id)
        self.cache.delete_memoized(affiliates_view.get_not_deleted_affiliates, affiliates_view, organization_id)

    def _delete_recruits_cache(self, recruits_view, organization_id: str, is_active: Optional[bool] = None,
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
        self.cache.delete_memoized(recruits_view.get_recruit, recruits_view, recruit_data)
        self.cache.delete_memoized(recruits_view.get_recruits_by_active_status, recruits_view,
                                   organization_id, is_active)
        self.cache.delete_memoized(recruits_view.get_recruits_by_deleted_status, recruits_view, organization_id,
                                   is_deleted)
        self.cache.delete_memoized(recruits_view.get_recruits_by_affiliate, recruits_view, affiliate_data)
        self.cache.delete_memoized(recruits_view.get_recruits_by_active_affiliate, recruits_view, affiliate_data,
                                   is_active)
        return True

    def _delete_services_cache(self, services_view, organization_id: str, service_id: str) -> bool:
        ***REMOVED***

        :param services_view:
        :param organization_id:
        :param service_id:
        :return:
        ***REMOVED***

        self.cache.delete_memoized(services_view.get_service, services_view, service_id, organization_id)
        self.cache.delete_memoized(services_view.return_services, services_view, organization_id)
        return True

    @staticmethod
    def _schedule_cache_deletion(func: Callable, kwargs: dict) -> None:
        ***REMOVED***
        **schedule_cache_deletion**
            schedule cache deletion such that it occurs sometime time in the future
        :param func:
        :param kwargs:
        :return:
        ***REMOVED***
        twenty_seconds_after: datetime = datetime_now() + timedelta(seconds=20)
        task_scheduler.add_job(func=func, trigger='date', run_date=twenty_seconds_after, kwargs=kwargs, id=create_id(),
                               name="cache_deletion", misfire_grace_time=360)


app_cache: CacheManager = CacheManager()
