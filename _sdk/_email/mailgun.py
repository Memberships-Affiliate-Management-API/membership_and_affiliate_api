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

from datetime import timedelta
import requests
from flask import current_app
from _cron.scheduler import task_scheduler
from config import config_instance
from typing import List, Optional,Callable
import aiohttp
import asyncio
from main import app_cache
from utils import return_ttl, datetime_now, create_id


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
                if json_data.get('status'):
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
        requests.post(url=self._mailgun_end_point, auth=api_instance,
                      data={"from": from_str, "to": to_str, "subject": subject, "text": text, "html": html,
                            "o:tag": o_tag})

        return True

    def return_organization_user(self, organization_id: str, uid: str) -> tuple:
        ***REMOVED***
        **return_organization_user**
        asynchronously returns organization data and user data
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        event_loop = asyncio.get_event_loop()
        tasks = [self.__get_user_data_async(organization_id=organization_id, uid=uid),
                 self.__get_organization_data_async(organization_id=organization_id)]
        results, _ = event_loop.run_until_complete(asyncio.wait(tasks))
        user_data_future, organization_data_future = results
        user_data: dict = user_data_future.result()
        organization_data: dict = organization_data_future.result()
        event_loop.close()
        return user_data, organization_data

    def _do_schedule_mail(self, to_email: str, subject: str, text: str, html: str) -> None:
        ***REMOVED***
            **_do_schedule_mail**
                using APScheduler schedule the emails to be sent at a later period

        :param to_email: email address to send the email to
        :param subject: subject of the email
        :param text: body in text format
        :param html: body in html format
        :return: does not return anything
        ***REMOVED***
        # Scheduling email to be sent later with mailgun api
        # Note: creating arguments dict
        _kwargs: dict = dict(to_list=[to_email], sbject=subject, text=text, html=html)
        # 5 seconds after now the email will be sent
        five_seconds_after = datetime_now() + timedelta(seconds=5)
        task_scheduler.add_job(func=self.__send_with_mailgun_rest_api, trigger='date', run_date=five_seconds_after,
                               kwargs=_kwargs, id=create_id(), name="do_schedule_mail_send", misfire_grace_time=360)

    @staticmethod
    def _base_email_scheduler(func: Callable, kwargs: dict) -> None:
        ***REMOVED***

        :param func:
        :param kwargs:
        :return:
        ***REMOVED***
        seconds_after = datetime_now() + timedelta(seconds=10)
        task_scheduler.add_job(func=func, trigger='date', run_date=seconds_after, kwargs=kwargs, id=create_id(),
                               name="base_email_scheduler", misfire_grace_time=360)
