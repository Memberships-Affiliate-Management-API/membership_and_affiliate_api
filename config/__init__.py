"""
    **Flask App Configuration Settings**
    *Python Version 3.8 and above*
    Used to setup environment variables for python flask app
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import os
import typing
# noinspection PyPackageRequirements
from decouple import config
import datetime


class Config:
    """
        **APP Configuration Settings**
            configuration variables for setting up the application
    """
    # TODO - Clean up configuration settings
    def __init__(self) -> None:
        # APP URLS
        self.BASE_URL: str = os.environ.get("BASE_URL") or config("BASE_URL")
        self.ADMIN_APP_BASEURL = os.environ.get("ADMIN_APP_BASEURL") or config("ADMIN_APP_BASEURL")
        self.CLIENT_APP_BASEURL = os.environ.get("CLIENT_APP_BASEURL") or config("CLIENT_APP_BASEURL")
        self.AUTH_URLS: list = [self.BASE_URL, self.ADMIN_APP_BASEURL, self.CLIENT_APP_BASEURL]

        # MAILGUN Keys
        self.MAILGUN_DOMAIN: str = os.environ.get("MAILGUN_DOMAIN") or config("MAILGUN_DOMAIN")
        self.MAILGUN_API_KEY: str = os.environ.get("MAILGUN_API_KEY") or config("MAILGUN_API_KEY")
        self.MAILGUN_NO_RESPONSE: str = os.environ.get("MAILGUN_NO_RESPONSE") or config("MAILGUN_NO_RESPONSE")
        self.MAILGUN_VALIDATION_KEY: str = os.environ.get("MAILGUN_VALIDATION_KEY") or config("MAILGUN_VALIDATION_KEY")
        self.MAILGUN_WEBHOOK_KEY: str = os.environ.get("MAILGUN_WEBHOOK_KEY") or config("MAILGUN_WEBHOOK_KEY")

        self.NO_RESPONSE_EMAIL: str = os.environ.get("NO_RESPONSE_EMAIL") or config("NO_RESPONSE_EMAIL")
        self.SMTP_SERVER_URI: str = os.environ.get("SMTP_SERVER_URI") or config("SMTP_SERVER_URI")
        self.SMTP_SERVER_PASSWORD: str = os.environ.get("SMTP_SERVER_PASSWORD") or config("SMTP_SERVER_PASSWORD")
        self.SMTP_SERVER_USERNAME: str = os.environ.get("SMTP_SERVER_USERNAME") or config("SMTP_SERVER_USERNAME")

        self.PROJECT: str = os.environ.get("PROJECT") or config("PROJECT")
        self.APP_NAME: str = os.environ.get("APP_NAME") or config("APP_NAME")

        self.ORGANIZATION_ID: str = os.environ.get("ORGANIZATION_ID") or config("ORGANIZATION_ID")
        self.ADMIN_UID: str = os.environ.get("ADMIN_UID") or config("ADMIN_UID")
        self.DEFAULT_ACCESS_RIGHTS: typing.List[str] = ["visitor", "user", "super_user", "admin"]
        self.ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL") or config("ADMIN_EMAIL")
        self.ADMIN_NAMES: str = os.environ.get("ADMIN_NAMES") or config("ADMIN_NAMES")
        self.ADMIN_SURNAME: str = os.environ.get("ADMIN_SURNAME") or config("ADMIN_SURNAME")
        self.ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD") or config("ADMIN_PASSWORD")
        self.ADMIN_CELL: str = os.environ.get("ADMIN_CELL") or config("ADMIN_CELL")

        self.PUBSUB_VERIFICATION_TOKEN = os.environ.get("PUBSUB_VERIFICATION_TOKEN") or config("PUBSUB_VERIFICATION_TOKEN")

        self.UTC_OFFSET = datetime.timedelta(hours=2)
        self.DATASTORE_TIMEOUT: int = 360  # seconds 6 minutes
        self.DATASTORE_RETRIES: int = 3  # total retries when saving to datastore

        self.CURRENCY: str = "USD"

        # TODO obtain correct paypal client ids
        self.PAYPAL_CLIENT_ID: str = os.environ.get("PAYPAL_CLIENT_ID") or config("PAYPAL_CLIENT_ID")
        self.PAYPAL_CLIENT_SECRET: str = os.environ.get("PAYPAL_CLIENT_SECRET") or config("PAYPAL_CLIENT_SECRET")
        self.PAYPAL_CLIENT_ID_SAND: str = os.environ.get("PAYPAL_CLIENT_ID_SAND") or config("PAYPAL_CLIENT_ID_SAND")
        self.PAYPAL_CLIENT_SECRET_SAND: str = os.environ.get("PAYPAL_CLIENT_SECRET_SAND") or config("PAYPAL_CLIENT_SECRET_SAND")

        self.GITHUB_CLIENT_ID: str = os.environ.get("GITHUB_CLIENT_ID") or config("GITHUB_CLIENT_ID")
        self.GITHUB_CLIENT_SECRET: str = os.environ.get("GITHUB_CLIENT_SECRET") or config("GITHUB_CLIENT_SECRET")

        self.IS_PRODUCTION: bool = True
        self.SECRET_KEY: str = os.environ.get("SECRET_KEY") or config("SECRET_KEY")
        self.DEBUG: bool = False

        self.CACHE_TYPE: str = "simple"
        self.CACHE_DEFAULT_TIMEOUT: int = 60 * 60 * 6
        self.MEM_CACHE_SERVER_URI: str = ""
        self.GOOGLE_APPLICATION_CREDENTIALS: str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or config("GOOGLE_APPLICATION_CREDENTIALS")

        self.PAYMENT_PLANS_SCHEDULES: typing.List[str] = ['monthly', 'quarterly', 'annually']
        self.PAYMENT_PLANS_PAYMENT_DAYS: typing.List[int] = [1, 2, 3, 4, 5]
        self.MINIMUM_WITHDRAWAL_AMOUNT_USD: int = 3000  # amount is in cents

        self.ENV: str = "production"
        self.TEMPLATES_AUTO_RELOAD: bool = True
        self.PREFERRED_URL_SCHEME: str = "https"

        # NOTE : setting IS_PRODUCTION here - could find a better way of doing this rather
        # than depending on the OS
        if "Windows_NT" == os.environ.get("OS"):
            self.DEBUG = True
            self.IS_PRODUCTION = False
            self.ENV = "development"
            self.PROPAGATE_EXCEPTIONS: bool = True
            self.PRESERVE_CONTEXT_ON_EXCEPTION: bool = True
            self.EXPLAIN_TEMPLATE_LOADING: bool = False
            self.PREFERRED_URL_SCHEME: str = "http"
            self.TESTING: bool = True
            # TODO - set Cache to MEM_CACHE and then setup the server URI, applicable on version 2

    def __str__(self) -> str:
        return '''PROJECT: {}, APP_NAME: {}, ORGANIZATION_ID: {}, DEFAULT_ACCESS_RIGHTS: {}, ADMIN_EMAIL: {}, 
        UTC_OFFSET: {}, PUBSUB_VERIFICATION_TOKEN: {}, DATASTORE_TIMEOUT: {}, DATASTORE_RETRIES: {}, CURRENCY: {},
        PAYPAL_CLIENT_ID: {}, PAYPAL_CLIENT_SECRET: {}, PAYPAL_CLIENT_ID_SAND: {} , PAYPAL_CLIENT_SECRET_SAND: {},
        IS_PRODUCTION: {}, SECRET_KEY: {}, DEBUG: {}, CACHE_TYPE: {}, CACHE_DEFAULT_TIMEOUT: {}, 
        MEM_CACHE_SERVER_URI: {} GOOGLE_APPLICATION_CREDENTIALS: {}'''.format(
            self.PROJECT, self.APP_NAME, self.ORGANIZATION_ID, self.DEFAULT_ACCESS_RIGHTS, self.ADMIN_EMAIL,
            self.UTC_OFFSET, self.PUBSUB_VERIFICATION_TOKEN, self.DATASTORE_TIMEOUT, self.DATASTORE_RETRIES,
            self.CURRENCY, self.PAYPAL_CLIENT_ID, self.PAYPAL_CLIENT_SECRET, self.PAYPAL_CLIENT_ID_SAND,
            self.PAYPAL_CLIENT_SECRET_SAND, self.IS_PRODUCTION, self.SECRET_KEY, self.DEBUG, self.CACHE_TYPE,
            self.CACHE_DEFAULT_TIMEOUT, self.MEM_CACHE_SERVER_URI, self.GOOGLE_APPLICATION_CREDENTIALS)

    def __repr__(self) -> str:
        return self.__str__()

    def cache_dict(self) -> dict:
        """
            Consider converting the cache to MEM_CACHE Type or Redis
            preferably host the cache as a docker instance on Cloud Run
        :return: dict
        """
        # TODO learn how to host redis cache on Heroku then change this logic so cache launches redis
        if not self.IS_PRODUCTION or os.environ.get('IS_HEROKU'):
            return {
                "CACHE_TYPE": "simple",
                "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT,
                "CACHE_KEY_PREFIX": "memberships_cache_"
            }
        else:
            user = os.environ.get("CACHE_REDIS_USER") or config("CACHE_REDIS_USER")
            password = os.environ.get("CACHE_REDIS_PASSWORD") or config("CACHE_REDIS_PASSWORD")
            redis_host = os.environ.get("CACHE_REDIS_HOST") or config("CACHE_REDIS_HOST")
            db = os.environ.get("CACHE_REDIS_DB") or config("CACHE_REDIS_DB")
            return {
                "CACHE_TYPE": "RedisCache",
                "CACHE_DEFAULT_TIMEOUT": self.CACHE_DEFAULT_TIMEOUT,
                "CACHE_KEY_PREFIX": "memberships_cache_",
                "CACHE_REDIS_HOST": redis_host,
                "CACHE_REDIS_PORT": 18391,
                "CACHE_REDIS_PASSWORD": password,
                "CACHE_REDIS_DB": db,
                "CACHE_REDIS_URL": "redis://{}:{}@{}/0".format(user, password, redis_host),
                "CACHE_OPTIONS": ""
            }

            # TODO: Note replace with a redis server connection url


config_instance: Config = Config()
# Note: Config is a singleton - this means it cannot be redeclared anywhere else
del Config
