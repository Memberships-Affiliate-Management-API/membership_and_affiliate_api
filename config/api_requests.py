***REMOVED***
    **api requests**
        this module will handle all requests from this application to other api's

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import asyncio
from typing import Optional, List
from _cron.scheduler import schedule_func
import aiohttp


class APIRequests:
    ***REMOVED***
        **Class APIRequests**
    ***REMOVED***

    def __init__(self, app):
        ***REMOVED***

        :param app:
        ***REMOVED***
        self._base_url: str = app.config.get('BASE_URL')
        self._secret_key: str = app.config.get('SECRET_KEY')
        self._responses: Optional[List[dict]] = None

    @staticmethod
    async def _async_request(_url, json_data, headers) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=_url, json=json_data, headers=headers) as response:
                response, _ = response
                json_data: dict = response.json()
                return json_data.get('payload') if json_data.get('status') else None

    def _request(self, _url: str, json_data: dict, headers: dict) -> None:
        ***REMOVED***
        :param _url:
        :param json_data:
        :param headers:
        :return:
        ***REMOVED***
        self._responses.append(asyncio.run(self._async_request(_url=_url, json_data=json_data, headers=headers)))

    def schedule_data_send(self, _endpoint: Optional[str], body: Optional[dict] = None):
        ***REMOVED***
        **schedule_data_send**
            schedule to send data without expecting a response, as
            responses will be stored on self._responses

        :param _endpoint:
        :param body:
        :return:
        ***REMOVED***
        _url: str = f'{self._base_url}{_endpoint}'
        if isinstance(body, dict):
            body.update(SECRET_KEY=self._secret_key)
        else:
            body: dict = dict(SECRET_KEY=self._secret_key)
        headers: dict = {'content-type': 'application/json'}
        _kwargs: dict = dict(_url=_url, json_data=body, headers=headers)

        schedule_func(func=self._request, kwargs=_kwargs)








