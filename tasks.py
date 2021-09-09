"""
    will start task scheduler as a service
"""
import asyncio
from schedulers.scheduler import task_scheduler


async def main():
    while True:
        all_jobs = task_scheduler.get_jobs()
        for job in all_jobs:
            print(f'Running Job : {job}')
            job.run()
            task_scheduler.cancel_job(job)
        await asyncio.sleep(30)


if __name__ == '__main__':
    print('Starting task scheduler')
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'exception : {str(e)}')

