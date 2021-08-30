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

from main import app_cache
from utils import timestamp, create_id, return_ttl


class APIRequests:
    ***REMOVED***
        **Class APIRequests**
            this class handles creating api calls then scheduling them and handles results as they are
            returned asynchronously.

        to make a request schedule a request with schedule_data_send
        obtain the request id then after a while check if the request has been returned with get_response
        using the _request_id
    ***REMOVED***

    def __init__(self, app):
        ***REMOVED***

        :param app:
        ***REMOVED***
        self._base_url: str = app.config.get('BASE_URL')
        self._secret_key: str = app.config.get('SECRET_KEY')
        self._responses_queue: Optional[List[dict]] = None
        self._event_loop = None

    @staticmethod
    async def _async_request(_url, json_data, headers) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=_url, json=json_data, headers=headers) as response:
                json_data: dict = await response.json()
                return json_data.get('payload') if json_data.get('status') else None

    def _request(self, _url: str, json_data: dict, headers: dict) -> None:
        ***REMOVED***
        :param _url:
        :param json_data:
        :param headers:
        :return:
        ***REMOVED***
        # obtain the _request_id to be used as an identifier for this request
        _request_id: str = headers.get('_request_id')
        response = asyncio.run(self._async_request(_url=_url, json_data=json_data, headers=headers))
        # compiling a response dict to contain the _request_id and the returned results of the request
        self._responses_queue.append(dict(_request_id=_request_id, response=response))

    def schedule_data_send(self, _endpoint: Optional[str], body: Optional[dict] = None) -> str:
        ***REMOVED***
        **schedule_data_send**
            schedule to send data without expecting a response, as
            responses will be stored on self._responses

        :param _endpoint:
        :param body:
        :return: str -> request_id
        ***REMOVED***
        _url: str = f'{self._base_url}{_endpoint}'
        if isinstance(body, dict):
            body.update(SECRET_KEY=self._secret_key)
        else:
            body: dict = dict(SECRET_KEY=self._secret_key)
        headers: dict = {'content-type': 'application/json'}
        _request_id: str = create_id()
        # updating the request headers with the _request_id
        headers.update(_request_id=_request_id)
        _kwargs: dict = dict(_url=_url, json_data=body, headers=headers)
        # Scheduling the request to run later and then continue
        schedule_func(func=self._request, kwargs=_kwargs)
        # returning the _request_id so it can be used to retrieve the results at a later stage
        return _request_id

    @app_cache.memoize(timeout=return_ttl('short'), cache_none=False)
    def get_response(self, request_id: str) -> Optional[dict]:
        ***REMOVED***
        **get_response**
            from responses_queue retrieve response
            as a result of caching a request can be obtained multiple times from response _queue as it would be cached
        :return: dict -> containing response or None
        ***REMOVED***
        if isinstance(self._responses_queue, list) and len(self._responses_queue):
            # at Best will return None if response not found
            return [_response.get('response') for _response in self._responses_queue
                    if _response.get('_request_id') == request_id][0] or None
        # Note: None results will not be cached
        return None
