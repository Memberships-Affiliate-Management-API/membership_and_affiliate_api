***REMOVED***
    **Main API View**
        Main View module to enable api calls for use in main memberships website
***REMOVED***
import json
import requests
from typing import Optional
from flask import current_app


class MainAPPAPIView:
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
        self._register_user_endpoint: str = "_api/v1/client/users/register"
        self._login_user_endpoint: str = "_api/v1/client/users/login"
        self._logout_user_endpoint: str = "_api/v1/client/users/logout"

    def send_login_request(self, email: Optional[str], password: Optional[str]) -> tuple:
        ***REMOVED***
            **send_login_request**
                this function will send a login request for main application via an api
        :param email: email to login with
        :param password: password
        :return: login auth-token
        ***REMOVED***
        _url: Optional[str] = "{}{}".format(self._base_url, self._login_user_endpoint)
        json_data = json.dumps(dict(email=email, password=password, organization_id=self._organization_id,
                                    SECRET_KEY=self._secret_key))
        response, status = requests.post(url=_url, json=json_data)
        return response, status

    def send_logout_request(self, email: Optional[str], token: Optional[str]) -> tuple:
        ***REMOVED***
            **send_logout_request**
                will send a logout request through the user api
        :param email:
        :param token:
        :return:
        ***REMOVED***
        _url: Optional[str] = "{}{}".format(self._base_url, self._logout_user_endpoint)
        json_data = json.dumps(dict(email=email, token=token, organization_id=self._organization_id,
                                    SECRET_KEY=self._secret_key))

        response, status = requests.post(url=_url, json=json_data)
        return response, status

    def send_register_request(self, email: Optional[str], cell: Optional[str], password:  Optional[str],
                              names: Optional[str], surname:  Optional[str]) -> tuple:
        ***REMOVED***
            **send_register_request**
                send a register request via an api
        :param email:
        :param cell:
        :param password:
        :param names:
        :param surname:
        :return: response as dict
        ***REMOVED***
        _url: Optional[str] = "{}{}".format(self._base_url, self._logout_user_endpoint)
        json_data = json.dumps(dict(email=email, cell=cell, password=password, names=names, surname=surname,
                                    organization_id=self._organization_id, SECRET_KEY=self._secret_key))

        response, status = requests.post(url=_url, json=json_data)
        return response, status

    def send_recovery_email(self, email: Optional[str]) -> tuple:
        ***REMOVED***

        :param email:
        :return:
        ***REMOVED***
        pass


    def add_contact_message(self):
        ***REMOVED***
            adds contact message
        :return:
        ***REMOVED***
        pass

    def get_contact_message(self):
        ***REMOVED***

        :return:
        ***REMOVED***
        pass
