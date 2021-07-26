
from flask import Blueprint, request, render_template, get_flashed_messages

memberships_main_bp = Blueprint('memberships_main', __name__)


@memberships_main_bp.route('/', methods=["GET"])
def memberships_main() -> tuple:
    return render_template('main/home.html')


@memberships_main_bp.route('/<path:path>', methods=["GET"])
def memberships_main_routes(path: str) -> tuple:
    if path == 'home':
        return render_template('main/home.html')
    elif path == 'index':
        return render_template('main/home.html')
    elif path == 'contact':
        return render_template('main/contact.html')
    elif path == 'login':
        return render_template('main/login.html')
    elif path == 'logout':
        return render_template('main/logout.html')
    elif path == 'subscribe':
        return render_template('main/subscribe.html')
    elif path == 'terms':
        return render_template('main/terms.html')
    elif path == 'robots.txt':
        return render_template('main/robots.txt')
    elif path == 'sitemap.xml':
        return render_template('main/sitemap.xml')
    elif path == 'favicon.ico':
        return render_template('main/favicon.ico')
    elif path == 'sw.js':
        return render_template('main/sw.js')


@memberships_main_bp.route('/demos/api/<path:path>', methods=["GET"])
def api_demos(path: str) -> tuple:
    if path == "demos":
        return render_template('main/demos/demos.html')
    elif path == "memberships":
        return render_template('main/demos/memberships.html')
    elif path == "organizations":
        return render_template('main/demos/organizations.html')
    elif path == "coupons":
        return render_template('main/demos/coupons.html')
    elif path == "users":
        return render_template('main/demos/users.html')
    elif path == "affiliates":
        return render_template('main/demos/affiliates.html')


@memberships_main_bp.route('/examples/sdk/<path:path>', methods=["GET"])
def sdk_examples(path: str) -> tuple:
    if path == "examples":
        return render_template('main/examples/sdk/examples.html')
