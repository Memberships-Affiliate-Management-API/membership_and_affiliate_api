"""
    **main api run module for memberships and affiliate api **

"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"
from threading import Thread
import json
import os
from flask import Response

from cache.cache_manager import app_cache
from config import config_instance
from config.use_context import use_context
from main import create_app
from utils.utils import is_development, today, return_ttl
from tasks import start_task
# TODO create separate run files for client api, admin api, and public_api
app = create_app(config_class=config_instance)

debug = is_development() and config_instance.DEBUG
# Press the green button in the gutter to run the script.
# TODO Add logs handler which can send all errors to memberships and Affiliate Management Slack Channel


@app.before_request
def create_thread() -> None:
    """
    **create_thread**
        this creates a thread specifically to deal with tasks which will be run after request has been processed
    :return: None
    """
    try:
        if not isinstance(app.tasks_thread, Thread):
            app.tasks_thread = Thread(target=start_task)
        return
    except AttributeError as e:
        pass
    finally:
        return


@app.after_request
@use_context
def start_thread(response: Response) -> Response:
    """
        **start thread**
            starting a separate thread to deal with tasks that where put aside during the request
    """
    try:
        if isinstance(app.tasks_thread, Thread) and not app.tasks_thread.is_alive():
            app.tasks_thread.start()
    except RuntimeError as e:
        app.tasks_thread = Thread(target=start_task)
        app.tasks_thread.start()
    return response


@app.route('/', methods=['GET', 'POST'])
def main():
    message: str = f'Welcome to Memberships & Affiliate Management API: Time: {today()}'
    return json.dumps(dict(status=True, message=message)), 200


@app.route('/redoc', methods=['GET', 'POST'])
@app_cache.cache.memoize(timeout=return_ttl('short'))
def redoc():
    message: str = f'Redoc Documentation coming soon'
    print(message)
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
