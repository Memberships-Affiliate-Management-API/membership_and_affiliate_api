***REMOVED***
**heroku cron module**
    1. will start cron scheduler as a service
    2. and then executes cron endpoints in order to start running cron services when the time for the service
    is reached

***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import asyncio
from typing import Optional
import aiohttp
from config import config_instance
from _cron.scheduler import cron_scheduler
from config.exceptions import status_codes


async def _async_request(_url, json_data, headers) -> Optional[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=_url, json=json_data, headers=headers) as response:
            json_data = await response.json()
            if json_data.get('status'):
                user_data: dict = json_data.get('payload')
                return user_data
            return None


def send_cron_request(_endpoint: str) -> None:
    ***REMOVED***
    **send_request**
        actually sends a  request to endpoints
    :param _endpoint: endpoint to send request to
    :return: None
    ***REMOVED***
    _base_url: str = config_instance.BASE_URL
    _url: str = f"{_base_url}{_endpoint}"
    organization_id: str = config_instance.ORGANIZATION_ID
    headers: dict = {'content-type': 'application/json'}
    json_data = dict(organization_id=organization_id, SECRET_KEY=config_instance.SECRET_KEY)
    asyncio.run(_async_request(_url=_url, json_data=json_data, headers=headers))


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=1)
def heroku_cron_affiliate_jobs() -> tuple:
    ***REMOVED***
        **cron_affiliate_jobs**
            executes cron jobs related to affiliates, recruits and affiliate earnings
        :return: tuple
    ***REMOVED***
    _endpoint: str = '_cron/v1/affiliates'
    send_cron_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=3)
def heroku_cron_memberships() -> tuple:
    ***REMOVED***
        **heroku_cron_memberships**
            executes tasks related to memberships, membership plans, services and products
        :return: tuple
    ***REMOVED***
    _endpoint: str = '_cron/v1/memberships'
    send_cron_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=5)
def heroku_cron_transactions() -> tuple:
    ***REMOVED***
    **heroku_cron_transactions**
        executes verified transactions and then settles them

    :return: tuple
    ***REMOVED***
    _endpoint: str = '_cron/v1/transactions'
    send_cron_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


@cron_scheduler.scheduled_job(trigger='cron', day_of_week='mon-sun', hour=7)
def heroku_cron_users() -> tuple:
    ***REMOVED***
        **heroku_cron_users**

        :return: tuple
    ***REMOVED***
    _endpoint: str = '_cron/v1/users'
    send_cron_request(_endpoint=_endpoint)
    return "OK", status_codes.status_ok_code


if __name__ == '__main__':
    cron_scheduler.start()
