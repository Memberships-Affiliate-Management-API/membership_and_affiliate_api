from flask import Flask
from flask_caching import Cache
from config import config_instance
from authlib.integrations.flask_client import OAuth
# TODO: consider upgrading the cache service from version 2 of this api
from utils import clear_cache
app_cache: Cache = Cache(config=config_instance.cache_dict())

default_timeout: int = 60 * 60 * 6

# github authenticate - enables developers to easily sign-up to our api
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


def create_app(config_class=config_instance):
    app = Flask(__name__, static_folder="app/resources/static", template_folder="app/resources/templates")
    app.config.from_object(config_class)

    app_cache.init_app(app=app, config=config_class.cache_dict())
    oauth.init_app(app=app, cache=app_cache)
    # user facing or public facing api's
    from _api.public_api.affiliates.routes import affiliates_bp
    from _api.public_api.users.routes import users_bp
    from _api.public_api.memberships.routes import memberships_bp
    from _api.public_api.coupons.routes import coupons_bp
    from _api.public_api.wallet.routes import wallet_bp
    from handlers.routes import default_handlers_bp
    # importing IPN
    from _ipn.email import email_ipn_bp
    from _ipn.paypal import paypal_ipn_bp
    from _ipn.heroku import heroku_ipn_bp

    # importing admin app blueprints
    from main.app.admin.routes.dashboard import admin_dashboard_bp
    from main.app.admin.routes.home import admin_bp

    # import client app blueprints
    from main.app.client.routes.dashboard import client_dashboard_bp
    from main.app.client.routes.home import client_home_bp

    # importing client api blueprints
    from _api.client_api.api.apikeys.routes import client_api_keys_bp
    from _api.client_api.api.github_users.routes import client_github_users_api_bp
    from _api.client_api.api.organization.routes import client_organizations_api_bp
    from _api.client_api.api.contact.routes import contact_api_bp
    from _api.client_api.api.users.routes import client_users_api_bp
    from _api.client_api.api.memberships.routes import memberships_client_api_bp

    # import main app blueprints
    from main.app.memberships_main.routes.routes import memberships_main_bp

    # importing main api
    from main.app.memberships_main.api.api import main_api_bp

    # admin api
    from _api.admin_api.api.users.users import admin_users_api_bp
    from _api.admin_api.api.organizations.organization import admin_organization_api_bp
    from _api.admin_api.api.memberships.memberships import membership_plans_admin_api_bp

    # Routes registrations
    app.register_blueprint(affiliates_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(memberships_bp)
    app.register_blueprint(coupons_bp)
    app.register_blueprint(wallet_bp)

    # registering IPN
    app.register_blueprint(email_ipn_bp)
    app.register_blueprint(paypal_ipn_bp)
    app.register_blueprint(heroku_ipn_bp)

    # admin app handlers
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_bp)

    # client app default_handlers_bp
    app.register_blueprint(client_dashboard_bp)
    app.register_blueprint(client_home_bp)

    # client app api handlers
    app.register_blueprint(client_api_keys_bp)
    app.register_blueprint(client_github_users_api_bp)
    app.register_blueprint(client_organizations_api_bp)

    # main app handlers
    app.register_blueprint(memberships_main_bp)

    # registering main api handlers
    app.register_blueprint(main_api_bp)

    # registering admin api users
    app.register_blueprint(admin_users_api_bp)
    app.register_blueprint(admin_organization_api_bp)
    app.register_blueprint(membership_plans_admin_api_bp)
    app.register_blueprint(contact_api_bp)
    app.register_blueprint(client_users_api_bp)
    app.register_blueprint(memberships_client_api_bp)

    # Error Handlers
    app.register_blueprint(default_handlers_bp)

    # Clear Cache
    if clear_cache(app=app, cache=app_cache):
        print("Cache Cleared and Starting")
    return app
