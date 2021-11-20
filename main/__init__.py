""""
        **main api entry module for memberships & affiliates Management API**
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import os

from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_cors import CORS
from schedulers.scheduler import task_scheduler, cron_scheduler
from cache.cache_manager import app_cache
from config import config_instance
import tasks

# github authenticate - enables developers to easily sign-up to our api
from v1api import register_v1_api
from v2api import register_v2_api

oauth = OAuth()
github_authorize = oauth.register(
    name='github',
    client_id=config_instance.GITHUB_CLIENT_ID,
    client_secret=config_instance.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'})


# TODO divide the public api offering and client api and also admin api to be offered as different micro-services
# noinspection DuplicatedCode
def create_app(config_class=config_instance):
    """
    :param config_class:
    :return:
    """
    app = Flask(__name__, static_folder="app/resources/static", template_folder="app/resources/templates")
    app.config.from_object(config_class)

    app_cache.init_app(app=app)
    oauth.init_app(app=app, cache=app_cache.cache)
    CORS(app)

    with app.app_context():
        app = register_v1_api(app)
        app = register_v2_api(app)
        app.tasks_thread = None

        return app
