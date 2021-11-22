from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from _swagger_api.wallet import WalletView

docs = FlaskApiSpec()


def register_v2_api(app):
    """
        this function only adds version 2 of the public facing API
        register v2 swagger compatible api here
    :param app:
    :return:
    """
    from _swagger_api.users import UserViewModel, UserListView, AuthViewModel
    api = Api(app)

    # User Endpoints
    api.add_resource(UserViewModel,
                     '/api/v2/user',
                     endpoint='create_user',
                     methods=['POST'])

    api.add_resource(UserViewModel,
                     '/api/v2/user',
                     endpoint='update_user',
                     methods=['PUT'])

    api.add_resource(UserViewModel,
                     '/api/v2/user/<string:organization_id>/<string:uid>',
                     endpoint='get_user',
                     methods=['GET'])

    # Wallet view endpoints

    # create new wallet
    api.add_resource(WalletView,
                     '/api/v2/wallet',
                     endpoint='create_wallet',
                     methods=['POST'])

    # get an exisiting wallet
    api.add_resource(WalletView,
                     '/api/v2/wallet/<string:organization_id>/<string:uid>',
                     endpoint='get_wallet',
                     methods=['GET'])

    # Authentication endpoints
    api.add_resource(AuthViewModel, '/api/v2/auth/login', endpoint='user_login', methods=['POST'])
    api.add_resource(AuthViewModel, '/api/v2/auth/logout', endpoint='user_logout', methods=['PUT'])

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Memberships & Affiliate Management API',
            version='0.1.1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0'
        ),
        'APISPEC_SWAGGER_URL': '/api',
        'APISPEC_SWAGGER_UI_URL': '/api-ui'

    })
    # registering documentation
    docs.init_app(app)
    docs.register(target=UserViewModel, endpoint='create_user')
    docs.register(target=UserViewModel, endpoint='update_user')
    docs.register(target=UserViewModel, endpoint='get_user')

    # Authentication Docs
    docs.register(target=AuthViewModel, endpoint='user_login')
    docs.register(target=AuthViewModel, endpoint='user_logout')

    # Wallet Docs
    docs.register(target=WalletView, endpoint='create_wallet')
    docs.register(target=WalletView, endpoint='get_wallet')

    return app
