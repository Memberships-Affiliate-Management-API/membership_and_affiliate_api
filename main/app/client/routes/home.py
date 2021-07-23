***REMOVED***
    this is a public route
***REMOVED***
from flask import Blueprint, request, url_for, render_template, get_flashed_messages

client_home_bp = Blueprint('client_home', __name__)


@client_home_bp.route('/client', methods=["GET"])
def client_home() -> tuple:
    return render_template('client/home.html')


