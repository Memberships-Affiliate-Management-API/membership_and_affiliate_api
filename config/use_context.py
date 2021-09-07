"""
    **Wrapper to handle application and ndb context**
        Should be used everytime a method which access ndb databases is being created or updated
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import functools
import json
from flask import current_app
from main import create_app
from config import config_instance
from google.cloud import ndb
from google.oauth2 import service_account
from utils.utils import is_development, is_heroku
import os

if is_development():
    # NOTE: Local development service key is saved on local drive
    credential_path = "C:\\gcp_credentials\\heroku.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def use_context(func):
    """
        **use_context**
            will insert ndb context for working with ndb. Cloud Databases
        **NOTE**
            functions/ methods needs to be wrapped by this wrapper when they interact with the database somehow

    :param func: function to wrap
    :return: function wrapped with ndb.context
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not current_app:
            app = create_app(config_class=config_instance)
            app.app_context().push()
        else:
            app = current_app

        if is_heroku():
            # NOTE: hosted in Heroku service key should be saved as environment variable in heroku
            app_credentials = json.loads(config_instance.GOOGLE_APPLICATION_CREDENTIALS)
            credentials = service_account.Credentials.from_service_account_info(app_credentials)
            client = ndb.Client(namespace="main", project=app.config.get('PROJECT'), credentials=credentials)
        else:
            # NOTE: could be GCP or another cloud environment
            client = ndb.Client(namespace="main", project=app.config.get('PROJECT'))
        # TODO - setup everything related to cache policy and all else here
        with client.context():
            return func(*args, **kwargs)
    return wrapper

