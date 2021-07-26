from flask import Blueprint, request, render_template, get_flashed_messages, make_response
memberships_main_bp = Blueprint('memberships_main', __name__)


@memberships_main_bp.route('/', methods=["GET"])
def memberships_main() -> tuple:
    return render_template('main/home.html'), 200


@memberships_main_bp.route('/<path:path>', methods=["GET"])
def memberships_main_routes(path: str) -> tuple:
    if path == 'home':
        return render_template('main/home.html'), 200
    elif path == 'index':
        return render_template('main/home.html'), 200
    elif path == 'contact':
        return render_template('main/contact.html'), 200
    elif path == 'login':
        return render_template('main/login.html'), 200
    elif path == 'logout':
        return render_template('main/logout.html'), 200
    elif path == 'subscribe':
        return render_template('main/subscribe.html'), 200
    elif path == 'forget':
        return render_template('main/forget.html'), 200
    elif path == 'terms':
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
        return render_template('main/favicon.ico')
    elif path == 'sw.js':
        response = make_response(render_template('main/scripts/sw.js'))
        response.headers['content-type'] = 'application/javascript'
        return response, 200


@memberships_main_bp.route('/demos/api/<path:path>', methods=["GET"])
def api_demos(path: str) -> tuple:
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


@memberships_main_bp.route('/examples/sdk/<path:path>', methods=["GET"])
def sdk_examples(path: str) -> tuple:
    if path == "examples":
        return render_template('main/examples/sdk/examples.html'), 200
