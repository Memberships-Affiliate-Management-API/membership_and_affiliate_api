import os
from decouple import config
import datetime


class Config:
    PROJECT = os.environ.get("PROJECT") or config("PROJECT")
    APP_NAME = os.environ.get("APP_NAME") or config("APP_NAME")
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

    def cache_dict(self) -> dict:
        ***REMOVED***
            Consider converting the cache to MEM_CACHE Type or Redis
            preferably host the cache as a docker instance on Cloud Run
        :return: dict
        ***REMOVED***
        if not self.IS_PRODUCTION:
            return {
                "CACHE_TYPE": self.CACHE_TYPE,
                "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT
            }
        else:
            # TODO: Respond with Cache Configuration for a production environment
            return {
                "CACHE_TYPE": self.CACHE_TYPE,
                "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT
            }


config_instance: Config = Config()