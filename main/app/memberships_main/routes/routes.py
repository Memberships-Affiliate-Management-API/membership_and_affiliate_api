from flask import Blueprint, request, render_template, get_flashed_messages, make_response, current_app, redirect, \
    url_for
from main import app_cache
from security.users_authenticator import logged_user
from utils.utils import return_ttl, can_cache

memberships_main_bp = Blueprint('memberships_main', __name__)


# noinspection PyTypeChecker
@memberships_main_bp.route('/', methods=["GET"])
@logged_user
@app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
def memberships_main(current_user) -> tuple:
    get_flashed_messages()
    if current_user and current_user.uid:
        return render_template('main/home.html', current_user=current_user), 200

    return render_template('main/home.html'), 200


# noinspection PyTypeChecker
@memberships_main_bp.route('/<path:path>', methods=["GET"])
@logged_user
@app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
def memberships_main_routes(current_user, path: str) -> tuple:
    get_flashed_messages()

    if path == 'home' or path == "home.html":
        if current_user and current_user.uid:
            return render_template('main/home.html', current_user=current_user), 200
        return render_template('main/home.html'), 200

    elif path == 'index' or path == "index.html":
        return render_template('main/home.html'), 200

    elif path == 'contact' or path == "contact.html":
        if current_user and current_user.uid:
            return render_template('main/contact.html', current_user=current_user), 200

        return render_template('main/contact.html'), 200

    elif path == 'login' or path == "login.html":

        if current_user and current_user.uid:
            return redirect(url_for('memberships_main.memberships_main_routes', path='logout'))
        return render_template('main/login.html'), 200

    elif path == 'logout' or path == "logout.html":
        if not current_user:
            return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

        return render_template('main/logout.html', current_user=current_user), 200

    elif path == 'subscribe' or path == "subscribe.html":
        if current_user and current_user.uid:
            return redirect(url_for('memberships_main.memberships_main_routes', path='logout'))

        return render_template('main/subscribe.html'), 200

    elif path == 'forget' or path == "forget.html":
        if current_user and current_user.uid:
            return redirect(url_for('client_dashboard.client_dashboard_routes', path='dashboard'))

        return render_template('main/forget.html'), 200

    elif path == 'terms' or path == "terms.html":
        return render_template('main/terms.html'), 200

    elif path == 'robots.txt':
        response = make_response('main/robots.txt')
        response.headers['content-type'] = 'text/plain'
        return response, 200

    elif path == 'sitemap.xml':
        response = make_response('main/sitemap.xml')
        response.headers['content-type'] = 'text/xml'
        return response, 200

    elif path == 'favicon.ico':
        response = make_response(render_template('main/favicon.ico'))
        response.headers['content-type'] = "img/ico"
        return response, 200

    elif path == 'sw.js':
        response = make_response(render_template('main/scripts/sw.js'))
        response.headers['content-type'] = 'application/javascript'
        return response, 200


# noinspection PyTypeChecker
@memberships_main_bp.route('/demos/api/<path:path>', methods=["GET"])
@logged_user
@app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
def api_demos(current_user, path: str) -> tuple:
    get_flashed_messages()
    if path == "demos":
        return render_template('main/demos/demos.html'), 200
    elif path == "memberships":
        return render_template('main/demos/memberships.html'), 200
    elif path == "organizations":
        return render_template('main/demos/organizations.html'), 200
    elif path == "coupons":
        return render_template('main/demos/coupons.html'), 200
    elif path == "users":
        return render_template('main/demos/users.html'), 200
    elif path == "affiliates":
        return render_template('main/demos/affiliates.html'), 200


# noinspection PyTypeChecker
@memberships_main_bp.route('/examples/sdk/<path:path>', methods=["GET"])
@logged_user
@app_cache.memoize(timeout=return_ttl('short'), unless=can_cache())
def sdk_examples(current_user, path: str) -> tuple:
    get_flashed_messages()
    if path == "examples":
        return render_template('main/examples/sdk/examples.html'), 200
