import functools
import json

from flask import current_app, jsonify
from main import create_app
from config import config_instance
from google.cloud import ndb
from google.oauth2 import service_account
from utils.utils import is_development, is_heroku
import os

if is_development():
    # NOTE: Local development service key is saved on local drive
    credential_path = "C:\\gcp_credentials\\affiliates.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def use_context(func):
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

