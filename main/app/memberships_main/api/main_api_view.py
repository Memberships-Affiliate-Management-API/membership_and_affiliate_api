***REMOVED***
    **Main API View**
        Main View module to enable api calls for use in main memberships website
***REMOVED***
import json

import requests
from typing import Optional
from flask import current_app


class MainAPIView:
    ***REMOVED***
        **Class MainAPIView**
            enables the main application to call its endpoints through main api calls
            especially on users and contacts

            this effectively decouples the main memberships application from the rest of the application
    ***REMOVED***

    def __init__(self):
        self._secret_key: str = current_app.config.get('SECRET_KEY')
        self._base_url: str = current_app.config.get('BASE_URL')
        self._organization_id: str = current_app.config.get('ORGANIZATION_ID')
        self._register_user_endpoint: str = "api/v1/auth/register"
        self._login_user_endpoint: str = "api/v1/auth/login"
        self._logout_user_endpoint: str = "api/v1/auth/logout"

    def send_login_request(self, email: Optional[str], password: Optional[str]):
        ***REMOVED***
            **send_login_request**
                this function will send a login request for main application via an api
        :param email: email to login with
        :param password: password
        :return: login auth-token
        ***REMOVED***
        _url: Optional[str] = "{}{}".format(self._base_url, self._login_user_endpoint)
        json_data = json.dumps(dict(email=email, password=password, SECRET_KEY=self._secret_key))
        response, status = requests.post(url=_url, json=json_data)

    def send_logout_request(self, email: Optional[str], token: Optional[str]) -> tuple:
        ***REMOVED***
            **send_logout_request**
                will send a logout request through the user api
        :param email:
        :param token:
        :return:
        ***REMOVED***
        pass


    def send_register_request(self, email: Optional[str], cell: Optional[str], password:  Optional[str],
                              names: Optional[str], surname:  Optional[str]):
        ***REMOVED***
            **send_register_request**
                send a register request via an api
        :param email:
        :param cell:
        :param password:
        :param names:
        :param surname:
        :return:
        ***REMOVED***
        pass

