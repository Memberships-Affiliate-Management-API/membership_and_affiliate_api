from flask import Flask
from flask_caching import Cache
from config import Config

# TODO find a way to insure errors are not cached

cache_affiliates: Cache = Cache(config={'CACHE_TYPE': 'simple'})
# Cache data for six hours- cached data should be volume data
# TODO - there should be a function to purge the cache when not needed
# but normally when the data-service is not being used it will shutdown and thereby auto purging cache
default_timeout: int = 60 * 60 * 6


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    cache_affiliates.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': default_timeout})

    from api.affiliates.routes import affiliates_bp
    from api.users.routes import users_bp
    from api.memberships.routes import memberships_bp
    from api.coupons.routes import coupons_bp
    from api.wallet.routes import wallet_bp
    from handlers.routes import default_handlers_bp
    # importing IPN
    from _ipn.email import email_ipn_bp
    from _ipn.paypal import paypal_ipn_bp

    app.register_blueprint(affiliates_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(memberships_bp)
    app.register_blueprint(coupons_bp)
    app.register_blueprint(wallet_bp)

    # registering IPN
    app.register_blueprint(email_ipn_bp)
    app.register_blueprint(paypal_ipn_bp)

    app.register_blueprint(default_handlers_bp)

    return app
