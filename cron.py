***REMOVED***
    will start cron scheduler as a service
***REMOVED***
import asyncio
from typing import Optional
import aiohttp
from config import config_instance
from _cron.scheduler import cron_scheduler
from config.exceptions import status_codes


async def __async_request(_url, json_data, headers) -> Optional[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=_url, json=json_data, headers=headers) as response:
            response, status = response
            json_data = response.json()
            if json_data.get('status'):
                user_data: dict = json_data.get('payload')
                return user_data
            return None


def send_request(_endpoint: str) -> None:
    _base_url: str = config_instance.BASE_URL
    _url: str = f"{_base_url}{_endpoint}"
    organization_id: str = config_instance.ORGANIZATION_ID
    headers: dict = {'content-type': 'application/json'}
    json_data = dict(organization_id=organization_id, SECRET_KEY=config_instance.SECRET_KEY)
    asyncio.run(__async_request(_url=_url, json_data=json_data, headers=headers))


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=1)
def heroku_cron_affiliate_jobs() -> tuple:
    ***REMOVED***
        **cron_affiliate_jobs**


        :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/affiliates'
    send_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=3)
def heroku_cron_memberships() -> tuple:
    ***REMOVED***
        **heroku_cron_memberships**

        :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/memberships'
    send_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=5)
def heroku_cron_transactions() -> tuple:
    ***REMOVED***

    :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/transactions'
    send_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=7)
def heroku_cron_users() -> tuple:
    ***REMOVED***
        **heroku_cron_users**

        :return:
    ***REMOVED***
    _endpoint: str = '_cron/v1/users'
    send_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


if __name__ == '__main__':
    cron_scheduler.start()
