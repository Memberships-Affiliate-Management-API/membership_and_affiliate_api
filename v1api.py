

def register_v1_api(app):
    # user facing or public facing api's
    from _api.public_api.affiliates.routes import affiliates_bp
    from _api.public_api.users.routes import users_bp
    from _api.public_api.memberships.routes import memberships_bp
    from _api.public_api.coupons.routes import coupons_bp
    from _api.public_api.wallet.routes import wallet_bp
    from _api.public_api.services.routes import services_public_api_bp

    from handlers.routes import default_handlers_bp
    # importing IPN
    from _ipn.email import email_ipn_bp
    from _ipn.paypal import paypal_ipn_bp
    from _ipn.heroku import heroku_ipn_bp

    # import client app blueprints
    # TODO remove this routes to Client Dashboard APP
    # from main.app.client.routes.dashboard import client_dashboard_bp
    # from main.app.client.routes.home import client_home_bp

    # importing client api blueprints
    from _api.client_api.api.apikeys.routes import client_api_keys_bp
    from _api.client_api.api.github_users.routes import client_github_users_api_bp
    from _api.client_api.api.organization.routes import client_organizations_api_bp
    from _api.client_api.api.contact.routes import contact_api_bp
    from _api.client_api.api.users.routes import client_users_api_bp
    from _api.client_api.api.memberships.routes import memberships_client_api_bp
    from _api.client_api.api.services.routes import services_client_api_bp

    # import main app blueprints
    # TODO remove to main application
    # from main.app.memberships_main.routes.routes import memberships_main_bp

    # admin api
    from _api.admin_api.api.users.users import admin_users_api_bp
    from _api.admin_api.api.organizations.organization import admin_organization_api_bp
    from _api.admin_api.api.memberships.memberships import membership_admin_api_bp
    from _api.admin_api.api.apikeys.apikeys import admin_api_keys_api_bp
    from _api.admin_api.api.affiliates.affiliates import admin_affiliates_api_bp
    from _api.admin_api.api.affiliates.recruits import admin_recruits_api_bp

    # v1 cron jobs
    from _cron.transactions import cron_transactions_bp
    from _cron.users import cron_users_bp
    from _cron.memberships import cron_memberships_bp
    from _cron.affiliates import cron_affiliate_bp

    from _ipn.micro_auth import microservices_ipn_bp

    # v1 public api routes
    app.register_blueprint(affiliates_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(memberships_bp)
    app.register_blueprint(coupons_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(services_public_api_bp)

    # v1 ipn routes
    app.register_blueprint(email_ipn_bp)
    app.register_blueprint(paypal_ipn_bp)
    app.register_blueprint(heroku_ipn_bp)

    # client app default_handlers_bp
    # app.register_blueprint(client_dashboard_bp)
    # app.register_blueprint(client_home_bp)

    # client app api handlers
    app.register_blueprint(client_api_keys_bp)
    app.register_blueprint(client_github_users_api_bp)
    app.register_blueprint(client_organizations_api_bp)
    app.register_blueprint(client_users_api_bp)
    app.register_blueprint(contact_api_bp)
    app.register_blueprint(services_client_api_bp)
    app.register_blueprint(memberships_client_api_bp)

    # registering admin api users
    app.register_blueprint(admin_users_api_bp)
    app.register_blueprint(admin_organization_api_bp)
    app.register_blueprint(membership_admin_api_bp)
    app.register_blueprint(admin_api_keys_api_bp)
    app.register_blueprint(admin_affiliates_api_bp)
    app.register_blueprint(admin_recruits_api_bp)

    # cron jobs
    app.register_blueprint(cron_transactions_bp)
    app.register_blueprint(cron_users_bp)
    app.register_blueprint(cron_memberships_bp)
    app.register_blueprint(cron_affiliate_bp)

    # Error Handlers
    app.register_blueprint(default_handlers_bp)

    app.register_blueprint(microservices_ipn_bp)
    return app