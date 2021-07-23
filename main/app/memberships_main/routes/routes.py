
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
    elif path == 'subscribe':
        return render_template('main/subscribe.html')
    elif path == 'robots.txt':
        return render_template('main/robots.txt')
    elif path == 'sitemap.xml':
        return render_template('main/sitemap.xml')


