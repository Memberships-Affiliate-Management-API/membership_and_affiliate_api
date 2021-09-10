"""
    **main api run module for memberships and affiliate api **

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import json
import os
from config import config_instance
from main import create_app
from utils.utils import is_development, today

# TODO create separate run files for client api, admin api, and public_api
app = create_app(config_class=config_instance)

debug = is_development() and config_instance.DEBUG
# Press the green button in the gutter to run the script.

# TODO Add logs handler which can send all errors to memberships and Affiliate Management Slack Channel


@app.route('/', methods=['GET', 'POST'])
def main():
    message: str = f'Welcome to Memberships & Affiliate Management API: Time: {today()}'
    return json.dumps(dict(status=True, message=message)), 200


@app.route('/redoc', methods=['GET', 'POST'])
def redoc():
    message: str = f'Redoc Documentation coming soon'
    return json.dumps(dict(status=True, message=message)), 200


@app.route('/warm-up', methods=['GET', 'POST'])
def warmup():
    message: str = f'Warmup Success'
    return json.dumps(dict(status=True, message=message)), 200


if __name__ == '__main__':
    if is_development():
        # NOTE: this is a development server
        app.run(debug=debug, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
    else:
        app.run(debug=debug, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
