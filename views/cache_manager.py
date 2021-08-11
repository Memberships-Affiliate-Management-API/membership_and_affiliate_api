***REMOVED***
    **Cache Management Module**

    Classes and methods to manage cache items
***REMOVED***
from main import app_cache


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
