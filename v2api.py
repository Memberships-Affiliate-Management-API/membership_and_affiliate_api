from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

docs = FlaskApiSpec()


def register_v2_api(app):
    """
        register v2 swagger compatible api here
    :param app:
    :return:
    """
    from _swagger_api.users import UserViewModel, UserListView, AuthViewModel
    api = Api(app)
    api.add_resource(UserViewModel, '/api/v2/user', endpoint='create_user', methods=['POST'])

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Memberships & Affiliate Management API',
            version='0.0.1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/api',
        'APISPEC_SWAGGER_UI_URL': '/api-ui'

    })
    # registering documentation
    docs.init_app(app)
    docs.register(target=UserViewModel, endpoint='create_user')
    return app

