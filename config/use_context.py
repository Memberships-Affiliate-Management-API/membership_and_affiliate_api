import functools
from flask import current_app
from main import create_app
from config import config_instance
from google.cloud import ndb
from utils.utils import is_development
import os

if is_development():
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
        client = ndb.Client(namespace="main", project=app.config.get('PROJECT'))
        # TODO - setup everything related to cache policy and all else here
        with client.context():
            return func(*args, **kwargs)
    return wrapper

