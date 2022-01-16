"""
    **user_jobs module**
        module used to run cron jobs related to user accounts

"""
import asyncio
from typing import List, Coroutine, Optional

from google.api_core.exceptions import RetryError
from google.cloud.ndb import toplevel, tasklet, Future, wait_all

from _sdk._email import Mailgun
from config.use_context import use_context
from database.users import UserModel
from utils import today, date_days_ago


class UserJobs(Mailgun):
    """
    **Class UserJobs**
        cron jobs for users

    """

    def __init__(self):
        super().__init__()

    @use_context
    @toplevel
    def run(self) -> None:
        login_reminders = yield self.send_login_reminders()

    @tasklet
    def do_send_login_reminder(self, user_instance: UserModel):
        """
            **do_send_login_reminder**
                send actual login reminder to user

        :param user_instance:
        :return:
        """
        uid: str = user_instance.uid
        organization_id: str = user_instance.organization_id
        org_data: Optional[dict] = asyncio.run(self._get_organization_data_async(organization_id=organization_id, uid=uid))
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

    @tasklet
    def send_login_reminders(self) -> Optional[List[Future]]:
        """
        **send_login_reminders**
            sends login reminders to users and developers
        :return: None
        """
        try:
            seven_days_ago = date_days_ago(days=7)
            users_list: List[UserModel] = [user for user in
                                           UserModel.query(UserModel.email_verified == True).fetch_async().get_result()
                                           if user.last_login_date < seven_days_ago]
        except RetryError as e:
            return None

        return [self.do_send_login_reminder(user_instance=user) for user in users_list]
