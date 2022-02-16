"""
**heroku cron module**
    1. will start cron scheduler as a service
    2. and then executes cron endpoints in order to start running cron services when the time for the service
    is reached
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import asyncio
from functools import wraps

from typing import Optional, Callable
import aiohttp
from config import config_instance
# noinspection PyUnresolvedReferences
from schedulers.scheduler import cron_scheduler, repeat, every, run_pending
# from config.exceptions import status_codes
from utils import timestamp


def cron_logger(func: Callable) -> Callable:
    """
        **log_cron_calls**
    """

    @wraps(func)
    def logger(*args, **kwargs) -> Callable:
        started: int = timestamp()
        _response: Optional[dict] = func(*args, **kwargs)
    return logger


async def _async_request(_url, json_data, headers) -> Optional[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=_url, json=json_data, headers=headers) as response:
            json_data = await response.json()
            if json_data.get('status'):
                cron_response: dict = json_data.get('payload')
                return cron_response
            return None


async def send_cron_request(_endpoint: str) -> Optional[None]:
    """
    **send_request**
        actually sends a  request to endpoints
    :param _endpoint: endpoint to send request to
    :return: None
    """
    _base_url: str = config_instance.BASE_URL
    _url: str = f"{_base_url}{_endpoint}"
    organization_id: str = config_instance.ORGANIZATION_ID
    headers: dict = {'content-type': 'application/json'}
    json_data = dict(organization_id=organization_id, SECRET_KEY=config_instance.CRON_SECRET,
                     domain=config_instance.CRON_DOMAIN)
    return await _async_request(_url=_url, json_data=json_data, headers=headers)


@cron_logger
def heroku_cron_affiliate_jobs() -> tuple:
    """
        **cron_affiliate_jobs**
            executes cron jobs related to affiliates, recruits and affiliate earnings
        :return: tuple
    """
    _endpoint: str = '_cron/v1/affiliates'
    return asyncio.run(send_cron_request(_endpoint=_endpoint)), 200


@cron_logger
def heroku_cron_memberships() -> tuple:
    """
        **heroku_cron_memberships**
            executes tasks related to memberships, membership plans, services and products
        :return: tuple
    """
    return asyncio.run(send_cron_request(_endpoint='_cron/v1/memberships')), 200


@cron_logger
def heroku_cron_transactions() -> tuple:
    """
    **heroku_cron_transactions**
        executes verified transactions and then settles them

    :return: tuple
    """
    return asyncio.run(send_cron_request(_endpoint='_cron/v1/transactions')), 200


@cron_logger
def heroku_cron_users() -> tuple:
    """
        **heroku_cron_users**
            runs cron jobs related to users

        :return: tuple
    """
    _endpoint: str = '_cron/v1/users'
    return asyncio.run(send_cron_request(_endpoint=_endpoint)), 200


def main():
    cron_scheduler.every().day.at(time_str='01:00').do(heroku_cron_affiliate_jobs)
    cron_scheduler.every().day.at(time_str='03:00').do(heroku_cron_memberships)
    cron_scheduler.every().day.at(time_str='05:00').do(heroku_cron_transactions)
    cron_scheduler.every().day.at(time_str='07:00').do(heroku_cron_users)
    while True:
        cron_scheduler.run_pending()


if __name__ == '__main__':
    print('STARTING CRON JOBS')
    try:
        main()
    except Exception as e:
        print(f'exception : {str(e)}')
