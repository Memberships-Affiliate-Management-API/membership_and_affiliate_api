***REMOVED***
    **Main Memberships & Affiliates Management API Website Routes**
        Routes for requests related to main website for Memberships & Affiliates Management API.
***REMOVED***
from typing import Optional

from flask import Blueprint, render_template, get_flashed_messages, make_response, redirect, url_for, flash
from config.exceptions import status_codes
from main import app_cache, github_authorize
from security.users_authenticator import logged_user
from utils.utils import return_ttl, can_cache
from views.github_auth import GithubAuthView

memberships_main_bp = Blueprint('memberships_main', __name__)


# noinspection PyTypeChecker
@memberships_main_bp.route('/', methods=["GET"])
@logged_user
@app_cache.cached(timeout=return_ttl('short'), unless=can_cache())
def memberships_main(current_user: Optional[dict]) -> tuple:
    ***REMOVED***
        Basic Main route for Memberships & Affiliates Management API Admin APP
        Errors are handled by an error handler, located in a separate blueprint

    :param current_user: Logged In User None Otherwise
    :return: template plus status code as a tuple
    ***REMOVED***
    get_flashed_messages()
    if isinstance(current_user, dict) and bool(current_user.get('uid')):
        return render_template('main/home.html', current_user=current_user), status_codes.status_ok_code

    return render_template('main/home.html'), status_codes.status_ok_code


# noinspection PyTypeChecker
@memberships_main_bp.route('/<path:path>', methods=["GET"])
@logged_user
@app_cache.cached(timeout=return_ttl('short'), unless=can_cache())
def memberships_main_routes(current_user: Optional[dict], path: str) -> tuple:
    ***REMOVED***
        @app_cache.memoize( ) caching the results of this function based on function
        parameters current user and path.

    :param current_user: user who has logged in, or None if no User has logged in
    :param path: the requested path
    :return: rendered_template plus status code
    ***REMOVED***
    get_flashed_messages()

    if path == 'home' or path == "home.html":
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return render_template('main/home.html', current_user=current_user), status_codes.status_ok_code
        return render_template('main/home.html'), status_codes.status_ok_code

    elif path == 'index' or path == "index.html":
        return render_template('main/home.html'), status_codes.status_ok_code

    elif path == 'contact' or path == "contact.html":
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return render_template('main/contact.html', current_user=current_user), status_codes.status_ok_code

        return render_template('main/contact.html'), status_codes.status_ok_code

    elif path == 'login' or path == "login.html":
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return redirect(url_for('memberships_main.memberships_main_routes', path='logout'))
        return render_template('main/login.html'), status_codes.status_ok_code

    elif path == 'login-with-github':
        redirect_url = url_for("memberships_main.memberships_main_routes", path="github-authorize", _external=True)
        print("redirect uri : {}".format(redirect_url))
        return github_authorize.authorize_redirect(redirect_url)

    if path == "github-authorize":
        token = github_authorize.authorize_access_token()
        resp = github_authorize.get('user', token=token)
        profile = resp.json()
        # do something with the token and profile
        print(profile, token)
        # with profile and token create new user once done redirect to main page
        profile.update(dict(token=token))
        github_user_view: GithubAuthView = GithubAuthView()
        response, _ = github_user_view.create_user(user_details=profile)

        # TODO remember to include flashed messages on templates
        if response.to_dict()['status']:
            message: str = "You have successfully logged in"
            flash(message)
            return redirect('/')

    elif path == 'logout' or path == "logout.html":
        if not isinstance(current_user, dict) or not bool(current_user.get('uid')):
            return redirect(url_for('memberships_main.memberships_main_routes', path='login'))

        return render_template('main/logout.html', current_user=current_user), status_codes.status_ok_code

    elif path == 'subscribe' or path == "subscribe.html":
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return redirect(url_for('memberships_main.memberships_main_routes', path='logout'))

        return render_template('main/subscribe.html'), status_codes.status_ok_code

    elif path == 'forget' or path == "forget.html":
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return redirect(url_for('client_dashboard.client_dashboard_routes', path='dashboard'))

        return render_template('main/forget.html'), status_codes.status_ok_code

    elif path == 'terms' or path == "terms.html":
        return render_template('main/terms.html'), status_codes.status_ok_code

    elif path == 'robots.txt':
        response = make_response('main/robots.txt')
        response.headers['content-type'] = 'text/plain'
        return response, status_codes.status_ok_code

    elif path == 'sitemap.xml':
        response = make_response('main/sitemap.xml')
        response.headers['content-type'] = 'text/xml'
        return response, status_codes.status_ok_code

    elif path == 'favicon.ico':
        response = make_response(render_template('main/favicon.ico'))
        response.headers['content-type'] = "img/ico"
        return response, status_codes.status_ok_code

    elif path == 'sw.js':
        response = make_response(render_template('main/scripts/sw.js'))
        response.headers['content-type'] = 'application/javascript'
        return response, status_codes.status_ok_code


# noinspection PyTypeChecker
@memberships_main_bp.route('/demos/api/<path:path>', methods=["GET"])
@logged_user
@app_cache.cached(timeout=return_ttl('short'), unless=can_cache())
def api_demos(current_user: Optional[dict], path: str) -> tuple:
    ***REMOVED***
       @app_cache.memoize() this will enable caching based on function arguments in this case current_user, and path

    :param current_user: the user making the request None if no user has logged in
    :param path: path being requested
    :return: a tuple containing rendered template and response code
    ***REMOVED***
    get_flashed_messages()
    if path == "demos":
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            # Note: user has logged in
            return render_template('main/demos/demos.html', current_user=current_user), status_codes.status_ok_code

        return render_template('main/demos/demos.html'), status_codes.status_ok_code

    elif path == "memberships":
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            # Note: User has logged in
            return render_template('main/demos/memberships.html',
                                   current_user=current_user), status_codes.status_ok_code

        return render_template('main/demos/memberships.html'), status_codes.status_ok_code

    elif path == "organizations":
        # Displays API Demos Related to Organizations
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return render_template('main/demos/organizations.html',
                                   current_user=current_user), status_codes.status_ok_code

        return render_template('main/demos/organizations.html'), status_codes.status_ok_code

    elif path == "coupons":
        # Displays API Demos related to coupons and coupons code
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return render_template('main/demos/coupons.html', current_user=current_user), status_codes.status_ok_code

        return render_template('main/demos/coupons.html'), status_codes.status_ok_code

    elif path == "users":
        # Displays API Demos related to Users
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return render_template('main/demos/users.html', current_user=current_user), status_codes.status_ok_code

        return render_template('main/demos/users.html'), status_codes.status_ok_code

    elif path == "affiliates":
        # Displays API Demos related to Affiliates
        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return render_template('main/demos/affiliates.html', current_user=current_user), status_codes.status_ok_code
        return render_template('main/demos/affiliates.html'), status_codes.status_ok_code


# noinspection PyTypeChecker
@memberships_main_bp.route('/examples/sdk/<path:path>', methods=["GET"])
@logged_user
@app_cache.cached(timeout=return_ttl('short'), unless=can_cache())
def sdk_examples(current_user: Optional[dict], path: str) -> tuple:
    ***REMOVED***
        @app_cache.memoize() will cache the results of the function based on current_user and path

    :param current_user: the user making the request None if user has not logged in
    :param path: the path being requested
    :return: render_template() plus status code as a tuple
    ***REMOVED***
    get_flashed_messages()
    if path == "examples":
        # TODO- need to display this once Front End and Back End SDKS are done at least
        #  Node.JS, Javascript and Python SDK's may be completed before this is displayed

        if isinstance(current_user, dict) and bool(current_user.get('uid')):
            return render_template('main/examples/sdk/examples.html',
                                   current_user=current_user), status_codes.status_ok_code

        return render_template('main/examples/sdk/examples.html'), status_codes.status_ok_code
