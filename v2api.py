from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from _swagger_api.wallet import WalletView
from _swagger_api.users import UserViewModel, UserListView, AuthViewModel

docs = FlaskApiSpec()


def add_wallet_endpoints(api: Api) -> Api:
    """
    **add_wallet_endpoints**
        will create wallet related endpoints
    :param api:
    :return: api
    """
    # create new wallet
    api.add_resource(WalletView, '/api/v2/wallet', endpoint='create_wallet', methods=['POST'])
    # get an existing wallet
    get_wallet_url: str = '/api/v2/wallet/<string:organization_id>/<string:uid>'
    api.add_resource(WalletView, get_wallet_url , endpoint='get_wallet', methods=['GET'])
    # update wallet
    api.add_resource(WalletView, '/api/v2/wallet', endpoint='update_wallet', methods=['PUT'])
    return api


def add_user_endpoints(api: Api) -> Api:
    """
        **add_user_endpoints**
            will add user related endpoints
    :param api:
    :return: Api
    """
    # Adds new User
    api.add_resource(UserViewModel, '/api/v2/user', endpoint='create_user', methods=['POST'])
    # Update existing user
    api.add_resource(UserViewModel, '/api/v2/user', endpoint='update_user', methods=['PUT'])
    # Get user record
    get_user_url: str = '/api/v2/user/<string:organization_id>/<string:uid>'
    api.add_resource(UserViewModel, get_user_url, endpoint='get_user', methods=['GET'])
    return api


def add_auth_endpoints(api: Api) -> Api:
    """
        **add_auth_endpoints**
            adds authentication related endpoints
    :param api:
    :return: APi
    """
    # login user
    api.add_resource(AuthViewModel, '/api/v2/auth/login', endpoint='user_login', methods=['POST'])
    # logout user
    api.add_resource(AuthViewModel, '/api/v2/auth/logout', endpoint='user_logout', methods=['PUT'])
    return api


def register_v2_api(app):
    """
    **register_v2_api**
        this function only adds version 2 of the public facing API
        register v2 swagger compatible api here
    :param app:
    :return:
    """
    api = Api(app)
    api = add_auth_endpoints(api=add_wallet_endpoints(api=add_user_endpoints(api=api)))

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
