"""
    **Main API View**
        Main View module to enable api calls for use in main memberships website
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

import requests
from typing import Optional
from flask import current_app, jsonify


class MainAPPAPIView:
    """
        **Class MainAPIView**
            enables the main application to call its endpoints through main api calls
            especially on users and contacts

            this effectively decouples the main memberships application from the rest of the application
    """

    def __init__(self):
        self._secret_key: str = current_app.config.get('SECRET_KEY')
        self._base_url: str = current_app.config.get('BASE_URL')
        self._organization_id: str = current_app.config.get('ORGANIZATION_ID')
        self._register_user_endpoint: str = "_api/v1/client/users/register"
        self._login_user_endpoint: str = "_api/v1/client/users/login"
        self._logout_user_endpoint: str = "_api/v1/client/users/logout"
        self._send_contact_message_endpoint: str = "_api/v1/client/contact/create"
        self._send_email_recovery_endpoint: str = "_api/v1/client/users/send-email-recovery"

    def send_login_request(self, email: Optional[str], password: Optional[str]) -> tuple:
        """
            **send_login_request**
                this function will send a login request for main application via an api
        :param email: email to login with
        :param password: password
        :return: login auth-token
        """
        _url: str = f'{self._base_url}{self._login_user_endpoint}'
        user_data: dict = dict(email=email, password=password, organization_id=self._organization_id,
                               SECRET_KEY=self._secret_key)

        response = requests.post(url=_url, json=user_data)
        return response.json(), response.status_code

    def send_logout_request(self, email: Optional[str], token: Optional[str]) -> tuple:
        """
            **send_logout_request**
                will send a logout request through the user api
        :param email:
        :param token:
        :return:
        """
        _url: str = f'{self._base_url}{self._logout_user_endpoint}'
        user_data: dict = dict(email=email, token=token, organization_id=self._organization_id,
                               SECRET_KEY=self._secret_key)

        response = requests.post(url=_url, json=user_data)
        return response.json(), response.status_code

    def send_register_request(self, email: Optional[str], cell: Optional[str], password:  Optional[str],
                              names: Optional[str], surname:  Optional[str]) -> tuple:
        """
            **send_register_request**
                send a register request via an api
        :param email:
        :param cell:
        :param password:
        :param names:
        :param surname:
        :return: response as dict
        """
        _url: Optional[str] = f'{self._base_url}{self._logout_user_endpoint}'
        user_data = dict(email=email, cell=cell, password=password, names=names, surname=surname,
                         organization_id=self._organization_id, SECRET_KEY=self._secret_key)

        response = requests.post(url=_url, json=user_data)
        return response.json(), response.status_code

    def send_recovery_email(self, email: Optional[str]) -> tuple:
        """

        :param email:
        :return:
        """
        _url: str = f'{self._base_url}{self._send_email_recovery_endpoint}'
        user_data: dict = dict(email=email, organization_id=self._organization_id, SECRET_KEY=self._secret_key)
        response = requests.post(url=_url, json=user_data)
        return response.json(), response.status_code

    def send_contact_message_request(self, contact_message: Optional[dict]) -> tuple:
        """
            **send_contact_message_request**
                send contact message to the api through an api request
        :return:
        """
        _url: str = f'{self._base_url}{self._send_contact_message_endpoint}'

        contact_message.update(organization_id=self._organization_id, SECRET_KEY=self._secret_key)
        # json_data = json.dumps(contact_message)
        # just pass dict without any modifications
        response = requests.post(url=_url, json=contact_message)
        return response.json(), response.status_code

    def get_contact_message(self):
        """

        :return:
        """
        _url: str = f'{self._base_url}{self._send_contact_message_endpoint}'

