from datetime import datetime
from random import choice
from google.cloud.ndb.exceptions import BadValueError
from pytest import raises
from database.mixins import AmountMixin, AddressMixin
from utils.utils import create_id, timestamp
from tests import int_positive
from database.users import UserModel
from werkzeug.security import check_password_hash

user_instance: UserModel = UserModel()


