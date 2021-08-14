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
import typing
from flask import jsonify
from config import config_instance
from config.exceptions import status_codes, error_codes
from typing import List
import aiohttp
import asyncio


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
        self.api = config_instance.MAILGUN_API_KEY
        self.end_point = "https://api.mailgun.net/v3/{}/messages".format(config_instance.MAILGUN_DOMAIN)
        self.no_response = config_instance.MAILGUN_NO_RESPONSE
        self._admin_get_user_endpoint = '_api/v1/admin/users/get'
        self._admin_get_membership_plan_endpoint = '_api/v1/admin/membership-plans/get'
        self._admin_get_organization_endpoint = '_api/v1/admin/organizations/get'

    @staticmethod
    async def __async_request(_url, json_data, headers) -> typing.Union[dict, None]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=_url, json=json_data, headers=headers) as response:
                response, status = response
                json_data = response.json()
                if json_data.get('status'):
                    user_data: dict = json_data.get('payload')
                    return user_data
                return None

    async def __get_user_data_async(self, organization_id: str, uid: str) -> typing.Union[dict, None]:
        ***REMOVED***
            from an api obtain user details related to the parameters
        :param organization_id: organization_id related to the user
        :param uid: uid of the user
        :return:
        ***REMOVED***
        _url: str = "{}{}".format(config_instance.BASE_URL, self._admin_get_user_endpoint)
        json_data = jsonify({'organization_id': organization_id, 'uid': uid})
        # TODO replace requests to make this async
        headers = {'content-type': 'application/json'}
        return asyncio.run(self.__async_request(_url=_url, json_data=json_data, headers=headers))

    async def __get_membership_data_async(self, organization_id: str, uid: str) -> typing.Union[dict, None]:
        ***REMOVED***
            from an api obtain membership plan details related to the parameters
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        _url: str = "{}{}".format(config_instance.BASE_URL, self._admin_get_membership_plan_endpoint)
        json_data = jsonify({'organization_id': organization_id, 'uid': uid})
        headers = {'content-type': 'application/json'}
        return asyncio.run(self.__async_request(_url=_url, json_data=json_data, headers=headers))

    async def __get_organization_data_async(self, organization_id: str, uid: str) -> typing.Union[dict, None]:
        ***REMOVED***
            returns the organization details based on the organization id and uid
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        _url: str = "{}{}".format(config_instance.BASE_URL, self._admin_get_organization_endpoint)
        json_data = jsonify({'organization_id': organization_id, 'uid': uid})
        headers = {'content-type': 'application/json'}
        return asyncio.run(self.__async_request(_url=_url, json_data=json_data, headers=headers))

    def __send_with_mailgun_rest_api(self, to_list: List[str], subject: str, text: str, html: str,
                                     o_tag: List[str] = None) -> tuple:
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
        from_str = "{} <{}>".format(config_instance.APP_NAME, self.no_response)
        to_str = to_list
        api_instance = ("api", "{}".format(self.api))
        # TODO feature development use an async call here
        response = requests.post(url=self.end_point,
                                 auth=api_instance,
                                 data={"from": from_str, "to": to_str,
                                       "subject": subject, "text": text, "html": html, "o:tag": o_tag})

        response_data = response.json()
        if response.status_code == 200:
            message: str = 'Successfully sent email'
            return jsonify({"status": True,
                            'message': message, 'payload': response_data.id}), status_codes.status_ok_code

        message: str = 'Unable to send email please try again later'
        return jsonify({"status": False, "message": message}), error_codes.remote_data_error
