***REMOVED***
    **user_jobs module**
        module used to run cron jobs related to user accounts

***REMOVED***
import asyncio
from typing import List, Coroutine, Optional
from _sdk._email import Mailgun
from database.users import UserModel
from utils import today, date_days_ago


class UserJobs(Mailgun):
    ***REMOVED***
    **Class UserJobs**
        cron jobs for users

    ***REMOVED***

    def __init__(self):
        super(UserJobs, self).__init__()

    def run(self) -> None:
        asyncio.run(self.send_login_reminders())

    async def do_send_login_reminder(self, user_instance: UserModel):
        ***REMOVED***
            **do_send_login_reminder**
                send actual login reminder to user

        :param user_instance:
        :return:
        ***REMOVED***
        uid: str = user_instance.uid
        organization_id: str = user_instance.organization_id
        org_data: Optional[dict] = await self._get_organization_data_async(organization_id=organization_id, uid=uid)
        subject: str = f"{org_data.get('organization_name')} We missed you"
        text: str = f'''
        Hi {user_instance.names} {user_instance.surname}
        
        This is a reminder that you still have an account in {org_data.get('organization_name')}
        If you need any assistance login in and or performing any other tasks please let us know
        
        Thank You
        {org_data.get('organization_name')} Team 
        {org_data.get('home_url')}         
        '''
        html: str = f'''
        <h3>Hi {user_instance.names} {user_instance.surname}</h3>
        
        <p>This is a reminder that you still have an account in {org_data.get('organization_name')}</p>
        <p>If you need any assistance login in and or performing any other tasks please let us know</p>
        
        <h3>Thank You</h3>
        <strong>{org_data.get('organization_name')} Team</strong> 
        <a href="{org_data.get('home_url')}">{org_data.get('home_url')}</a>
        '''
        self._do_schedule_mail(to_email=user_instance.email, subject=subject, text=text, html=html)

    async def send_login_reminders(self) -> None:
        ***REMOVED***
        **send_login_reminders**
            sends login reminders to users and developers
        :return: None
        ***REMOVED***
        seven_days_ago = date_days_ago(days=7)
        users_list: List[UserModel] = [user for user in UserModel.query(UserModel.email_verified == True).fetch_async()
                                       if user.last_login_date < seven_days_ago]

        cron_jobs: List[Coroutine] = [self.do_send_login_reminder(user_instance=user) for user in users_list]
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(asyncio.gather(cron_jobs))
        event_loop.close()

