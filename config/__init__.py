import os
# noinspection PyPackageRequirements
from decouple import config
import datetime


class Config:
    PROJECT = os.environ.get("PROJECT") or config("PROJECT")
    APP_NAME = os.environ.get("APP_NAME") or config("APP_NAME")
    ORGANIZATION_ID = os.environ.get("ORGANIZATION_ID") or config("ORGANIZATION_ID")
    DEFAULT_ACCESS_RIGHTS = ["visitor", "user", "super_user", "admin"]
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL") or config("ADMIN_EMAIL")
    UTC_OFFSET = datetime.timedelta(hours=2)
    PUBSUB_VERIFICATION_TOKEN = os.environ.get("PUBSUB_VERIFICATION_TOKEN") or config("PUBSUB_VERIFICATION_TOKEN")
    DATASTORE_TIMEOUT: int = 360  # seconds
    DATASTORE_RETRIES: int = 3  # total retries when saving to datastore
    CURRENCY: str = "USD"
    PAYPAL_CLIENT_ID: str = os.environ.get("PAYPAL_CLIENT_ID") or config("PAYPAL_CLIENT_ID")
    PAYPAL_CLIENT_SECRET: str = os.environ.get("PAYPAL_CLIENT_SECRET") or config("PAYPAL_CLIENT_SECRET")
    PAYPAL_CLIENT_ID_SAND: str = os.environ.get("PAYPAL_CLIENT_ID_SAND") or config("PAYPAL_CLIENT_ID_SAND")
    PAYPAL_CLIENT_SECRET_SAND: str = os.environ.get("PAYPAL_CLIENT_SECRET_SAND") or config("PAYPAL_CLIENT_SECRET_SAND")
    IS_PRODUCTION: bool = True
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or config("SECRET_KEY")
    DEBUG: bool = False
    CACHE_TYPE: str = "simple"
    CACHE_DEFAULT_TIMEOUT: int = 60 * 60 * 6
    MEM_CACHE_SERVER_URI: str = ""

    def __init__(self) -> None:
        # TODO : set config IS_PRODUCTION Automatically here, may use any of several ways, consider setting DEBUG Also
        if "Windows_NT" == os.environ.get("OS"):
            self.DEBUG = True
            self.IS_PRODUCTION = False
            # TODO - set Cache to MEM_CACHE and then setup the server URI, applicable on version 2

    def __str__(self) -> str:
        return '''PROJECT: {}, APP_NAME: {}, ORGANIZATION_ID: {}, DEFAULT_ACCESS_RIGHTS: {}, ADMIN_EMAIL: {}, 
        UTC_OFFSET: {}, PUBSUB_VERIFICATION_TOKEN: {}, DATASTORE_TIMEOUT: {}, DATASTORE_RETRIES: {}, CURRENCY: {},
        PAYPAL_CLIENT_ID: {}, PAYPAL_CLIENT_SECRET: {}, PAYPAL_CLIENT_ID_SAND: {} , PAYPAL_CLIENT_SECRET_SAND: {},
        IS_PRODUCTION: {}, SECRET_KEY: {}, DEBUG: {}, CACHE_TYPE: {}, CACHE_DEFAULT_TIMEOUT: {}, 
        MEM_CACHE_SERVER_URI: {}'''.format(
            self.PROJECT, self.APP_NAME, self.ORGANIZATION_ID, self.DEFAULT_ACCESS_RIGHTS, self.ADMIN_EMAIL,
            self.UTC_OFFSET, self.PUBSUB_VERIFICATION_TOKEN, self.DATASTORE_TIMEOUT, self.DATASTORE_RETRIES,
            self.CURRENCY, self.PAYPAL_CLIENT_ID, self.PAYPAL_CLIENT_SECRET, self.PAYPAL_CLIENT_ID_SAND,
            self.PAYPAL_CLIENT_SECRET_SAND, self.IS_PRODUCTION, self.SECRET_KEY, self.DEBUG, self.CACHE_TYPE,
            self.CACHE_DEFAULT_TIMEOUT, self.MEM_CACHE_SERVER_URI)

    def __repr__(self) -> str:
        return self.__str__()

    def cache_dict(self) -> dict:
        ***REMOVED***
            Consider converting the cache to MEM_CACHE Type or Redis
            preferably host the cache as a docker instance on Cloud Run
        :return: dict
        ***REMOVED***
        if not self.IS_PRODUCTION or os.environ.get('IS_HEROKU'):
            return {
                "CACHE_TYPE": "simple",
                "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT,
                "CACHE_KEY_PREFIX": "memberships_cache_"
            }
        else:
            # TODO: Respond with Cache Configuration for a production environment
            user = os.environ.get("CACHE_REDIS_USER") or config("CACHE_REDIS_USER")
            password = os.environ.get("CACHE_REDIS_PASSWORD") or config("CACHE_REDIS_PASSWORD")
            redis_host = os.environ.get("CACHE_REDIS_HOST") or config("CACHE_REDIS_HOST")
            db = os.environ.get("CACHE_REDIS_DB") or config("CACHE_REDIS_DB")
            return {
                "CACHE_TYPE": "redis",
                "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT,
                "CACHE_KEY_PREFIX": "memberships_cache_",
                "CACHE_REDIS_HOST": "{}".format(redis_host),
                "CACHE_REDIS_PORT": 6379,
                "CACHE_REDIS_PASSWORD": "{}".format(password),
                "CACHE_REDIS_DB": "{}".format(db),
                "CACHE_REDIS_URL": "{}{}@{}:6379/2".format(user, password, redis_host),
                "CACHE_OPTIONS": ""
            }

            # TODO: Note replace with a redis server connection url


config_instance: Config = Config()
