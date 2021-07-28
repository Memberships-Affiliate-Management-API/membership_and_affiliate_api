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
    IS_PRODUCTION: bool = False
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or config("SECRET_KEY")
    DEBUG: bool = True





