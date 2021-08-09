from flask import Flask
from flask_caching import Cache
from config import config_instance

# TODO: consider upgrading the cache service from version 2 of this api
app_cache: Cache = Cache(config=config_instance.cache_dict())
# TODO: problems will arise with a simple cache implementation where there are moreEl
#  than one instance of this api, as one of the instance may or will hold different
#  or stale data on cache and serve this data to the clients, and users.

default_timeout: int = 60 * 60 * 6


def create_app(config_class=config_instance):
    app = Flask(__name__, static_folder="app/resources/static", template_folder="app/resources/templates")
    app.config.from_object(config_class)

    app_cache.init_app(app=app, config=config_class.cache_dict())

    from _api.affiliates.routes import affiliates_bp
    from _api.users.routes import users_bp
    from _api.memberships.routes import memberships_bp
    from _api.coupons.routes import coupons_bp
    from _api.wallet.routes import wallet_bp
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

    # import main app blueprints
    from main.app.memberships_main.routes.routes import memberships_main_bp

    # importing main api
    from main.app.memberships_main.api.api import main_api_bp

    # admin api
    from main.app.admin.api.users.users import admin_users_api_bp
    from main.app.admin.api.organizations.organization import admin_organization_api_bp
    from main.app.admin.api.memberships.memberships import membership_plans_admin_api_bp

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

    # main app handlers
    app.register_blueprint(memberships_main_bp)

    # registering main api handlers
    app.register_blueprint(main_api_bp)

    # registering admin api users
    app.register_blueprint(admin_users_api_bp)
    app.register_blueprint(admin_organization_api_bp)
    app.register_blueprint(membership_plans_admin_api_bp)

    # Error Handlers
    app.register_blueprint(default_handlers_bp)
    print(app.config)

    return app
