***REMOVED***
    **Mailgun Emails Integration SDK**
        *Python ^3.8
    ***REMOVED***
        ***REMOVED***
        ***REMOVED***
        ***REMOVED***

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import requests
from flask import jsonify, current_app
from config import config_instance
from config.exceptions import status_codes, error_codes
from typing import List, Optional
import aiohttp
import asyncio

from main import app_cache
from utils import return_ttl


class Mailgun:
    ***REMOVED***
        **MailGun**
            methods to integrate Mailgun Emailing rest API with Memberships & Affiliates APIKeys
            for the purposes of sending notifications and emails on behalf of clients.

        TODO - feature development add Mailgun Templates see Email-templates on Github Repos
    ***REMOVED***

    def __init__(self):
        ***REMOVED***
            mailgun_domain : domain name registered with mailgun
            MAILGUN_API_KEY : can be found from mailgun control panel
        ***REMOVED***
        self._base_url: str = config_instance.BASE_URL
        self._mailgun_api_key = config_instance.MAILGUN_API_KEY
        self._mailgun_end_point = "https://api.mailgun.net/v3/{}/messages".format(config_instance.MAILGUN_DOMAIN)
        self._mailgun_no_response_email = config_instance.MAILGUN_NO_RESPONSE
        self._admin_get_user_endpoint = '_api/v1/admin/users/get'
        self._admin_get_membership_plan_endpoint = '_api/v1/admin/membership-plans/get'
        self._admin_get_organization_endpoint = '_api/v1/admin/organizations/get'
        self._secret_key: str = current_app.config.get('SECRET_KEY')

    # TODO - replace requests with this all over the application
    @staticmethod
    async def __async_request(_url, json_data, headers) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=_url, json=json_data, headers=headers) as response:
                response, status = response
                json_data = response.json()
                if json_data.get('status') is True:
                    user_data: dict = json_data.get('payload')
                    return user_data
                return None

    @app_cache.memoize(timeout=return_ttl('short'))
    async def __get_user_data_async(self, organization_id: str, uid: str) -> Optional[dict]:
        ***REMOVED***
            from an api obtain user details related to the parameters
        :param organization_id: organization_id related to the user
        :param uid: uid of the user
        :return:
        ***REMOVED***
        _url: str = f'{self._base_url}{self._admin_get_user_endpoint}'
        json_data = dict(organization_id=organization_id, uid=uid, SECRET_KEY=self._secret_key)
        headers = {'content-type': 'application/json'}
        return await self.__async_request(_url=_url, json_data=json_data, headers=headers)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def __get_membership_data_async(self, organization_id: str, uid: str) -> Optional[dict]:
        ***REMOVED***
            **__get_membership_data_async**
                asynchronously from an api obtain membership plan details related to the parameters
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        _url: str = f'{self._base_url}{self._admin_get_membership_plan_endpoint}'
        json_data = dict(organization_id=organization_id, uid=uid, SECRET_KEY=self._secret_key)
        headers = {'content-type': 'application/json'}
        return await self.__async_request(_url=_url, json_data=json_data, headers=headers)

    @app_cache.memoize(timeout=return_ttl('short'))
    async def __get_organization_data_async(self, organization_id: str) -> Optional[dict]:
        ***REMOVED***
            **__get_organization_data**
                asynchronously returns the organization details based on the organization id and uid
        :param organization_id:
        :return:
        ***REMOVED***
        # TODO ensure this endpoints works
        _url: str = f'{config_instance.BASE_URL}{self._admin_get_organization_endpoint}'
        json_data = dict(organization_id=organization_id, SECRET_KEY=self._secret_key)
        headers = {'content-type': 'application/json'}
        return await self.__async_request(_url=_url, json_data=json_data, headers=headers)

    def __send_with_mailgun_rest_api(self, to_list: List[str], subject: str, text: str, html: str,
                                     o_tag: List[str] = None) -> bool:
        ***REMOVED***
        **__send_with_mailgun_rest_api**
            a method to send email via rest api

        :param o_tag:  message o tag | format of o:tag  ["September newsletter", "newsletters"]
        :param to_list: list of email addresses to send this email format ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"]
        :param subject: the subject of the email
        :param text: the text part of the email
        :param html: the html part of the email
        :return: tuple indicating the status of the message sent
        ***REMOVED***
        # NOTE: from mail must be registered with MAILGUN
        from_str = f'{config_instance.APP_NAME} <{self._mailgun_no_response_email}>'
        to_str = to_list
        api_instance = ("api", "{}".format(self._mailgun_api_key))
        # TODO feature development use an async call here
        response = requests.post(url=self._mailgun_end_point,
                                 auth=api_instance,
                                 data={"from": from_str, "to": to_str,
                                       "subject": subject, "text": text, "html": html, "o:tag": o_tag})

        return True
