from typing import Optional, List, Union
from flask import jsonify
from google.cloud import ndb

from _sdk._email import Mailgun
from config.exceptions import status_codes, DataServiceError, error_codes, UnAuthenticatedError
from database.helpdesk import HelpDeskValid, TicketValid, TicketThreadValid, Ticket
from database.helpdesk import HelpDesk
from utils import create_id
from config.exception_handlers import handle_view_errors
from config.use_context import use_context
import re
import functools


class Validators(HelpDeskValid, TicketValid, TicketThreadValid):
    """
        helpdesk input validators
    """

    def __init__(self):
        super(Validators, self).__init__()

    @staticmethod
    def is_user(uid: str) -> bool:
        """
            TODO find out if uid contains valid user
        """

        return True

    @staticmethod
    async def is_user_async(uid: str) -> bool:
        return True

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """
            TODO - check if user owns email
            TODO - or if email is being used by another user
        """
        regex = '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
        return True if re.search(regex, email) is not None else False

    @staticmethod
    def is_cell_valid(cell: str) -> bool:
        """
            TODO - check if user owns cell
            TODO - or if cell is being used by another user
        """
        pass

    @staticmethod
    async def is_cell_valid_async(cell: str) -> bool:
        """
            TODO - check if user owns cell
            TODO - or if cell is being used by another user
        """
        pass

    def is_ticket_valid(self, uid: str, topic: str, subject: str, message: str, email: str, cell: str) -> bool:
        """
            TODO- validate ticket
        """
        valid_user: bool = self.is_user(uid=uid)
        valid_topic: bool = self.is_topic_valid(topic=topic)
        valid_subject: bool = self.is_subject_valid(subject=subject)
        valid_message: bool = self.is_message_valid(message=message)
        valid_email: bool = self.is_email_valid(email=email)
        valid_cell: bool = self.is_cell_valid(cell=cell)
        return valid_user and valid_topic and valid_subject and valid_message and valid_email and valid_cell


# noinspection DuplicatedCode
class HelpDeskView(Validators):

    def __init__(self):
        super(HelpDeskView, self).__init__()

    @use_context
    @handle_view_errors
    def create_help_desk(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'help desk already created'}), 200
        help_desk_instance = HelpDesk()
        key: Optional[ndb.Key] = help_desk_instance.put()
        if not bool(key):
            return jsonify({'status': False, 'message': 'Error updating database'}), status_codes.data_not_found_code
        return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                        'message': 'help desk created'}), 200

    @use_context
    @handle_view_errors
    async def create_help_desk_async(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'help desk already created'}), 200
        help_desk_instance = HelpDesk()
        key: Optional[ndb.Key] = help_desk_instance.put()
        if not bool(key):
            return jsonify({'status': False, 'message': 'Error updating database'}), status_codes.data_not_found_code
        return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                        'message': 'help desk created'}), 200

    @use_context
    @handle_view_errors
    @functools.lru_cache(maxsize=1)
    def get_help_desk(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'successfully fetched helpdesk'}), 200

        return jsonify({'status': False, 'message': 'unable to find helpdesk'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    @functools.lru_cache(maxsize=1)
    async def get_help_desk_async(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'successfully fetched helpdesk'}), 200

        return jsonify({'status': False, 'message': 'unable to find helpdesk'}), status_codes.data_not_found_code

    @use_context
    def add_ticket(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            help_desk_instance.total_tickets += 1
            help_desk_instance.total_tickets_opened += 1
            help_desk_instance.put()
            return True
        return False

    @use_context
    async def add_ticket_async(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            help_desk_instance.total_tickets += 1
            help_desk_instance.total_tickets_opened += 1
            help_desk_instance.put()
            return True
        return False

    @use_context
    def close_ticket(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            help_desk_instance.total_tickets_opened -= 1
            help_desk_instance.total_tickets_closed += 1
            help_desk_instance.put()
            return True
        return False

    @use_context
    async def close_ticket_async(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
        if isinstance(help_desk_instance, HelpDesk) and bool(help_desk_instance):
            help_desk_instance.total_tickets_opened -= 1
            help_desk_instance.total_tickets_closed += 1
            help_desk_instance.put_async().get_result()
            return True
        return False


class TicketsMessaging(Mailgun):
    """
        **Class TicketsMessaging**
    """

    def __init__(self) -> None:
        super(TicketsMessaging, self).__init__()

    def _send_ticket_response(self, ticket_id: str, subject: str, message: str) -> None:
        pass

    def _send_sms_notifications(self, ticket_id: str, subject: str, message: str) -> None:
        pass


# noinspection DuplicatedCode
class TicketView(Validators, TicketsMessaging):
    """
    **Class TicketView**
        class used to work with tickets, and access data
    """

    def __init__(self):
        super(TicketView, self).__init__()

    @use_context
    @handle_view_errors
    def create_ticket(self, uid: str, topic: str, subject: str, message: str, email: str,
                      cell: str) -> tuple:
        if self.is_ticket_valid(uid=uid, topic=topic, subject=subject, message=message, email=email,
                                cell=cell):
            ticket_instance: Ticket = Ticket()
            ticket_instance.ticket_id = create_id()
            ticket_instance.uid = uid
            ticket_instance.topic = topic
            ticket_instance.subject = subject
            ticket_instance.message = message
            ticket_instance.email = email
            ticket_instance.cell = cell
            key: Optional[ndb.Key] = ticket_instance.put()

            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully created ticket'}), status_codes.successfully_updated_code

        message: str = "User Not Authorized: to update ticket"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    @use_context
    @handle_view_errors
    async def create_ticket_async(self, uid: str, topic: str, subject: str, message: str,
                                  email: str, cell: str) -> tuple:

        if self.is_ticket_valid(uid=uid, topic=topic, subject=subject, message=message,
                                email=email, cell=cell):

            ticket_instance: Ticket = Ticket()
            ticket_instance.ticket_id = create_id()
            ticket_instance.uid = uid
            ticket_instance.topic = topic
            ticket_instance.subject = subject
            ticket_instance.message = message
            ticket_instance.email = email
            ticket_instance.cell = cell
            key: Optional[ndb.Key] = ticket_instance.put_async().get_result()

            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully created ticket'}), status_codes.successfully_updated_code

        message: str = "User Not Authorized: to update ticket"
        raise UnAuthenticatedError(status=error_codes.un_auth_error_code, description=message)

    @use_context
    @handle_view_errors
    def resolve_ticket(self, ticket_id: str) -> tuple:
        """
            ticket_id: str
            return: resolved ticket
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):
            ticket_instance.is_resolved = True
            key: Optional[ndb.Key] = ticket_instance.put()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully resolved ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Ticket not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def resolve_ticket_async(self, ticket_id: str) -> tuple:
        """
            ticket_id: str
            return: resolved ticket
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):
            ticket_instance.is_resolved = True
            key: Optional[ndb.Key] = ticket_instance.put_async().get_result()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully resolved ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Ticket not found'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def update_ticket(self, ticket_id: Optional[str], topic: Optional[str] = None,
                      subject: Optional[str] = None, message: Optional[str] = None,
                      email: str = Optional[str], cell: Optional[str] = None,
                      assigned_to_uid: Optional[str] = None) -> tuple:

        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):
            if topic is not None:
                ticket_instance.topic = topic
            if subject is not None:
                ticket_instance.subject = subject
            if message is not None:
                ticket_instance.message = message
            if email is not None:
                ticket_instance.email = email
            if cell is not None:
                ticket_instance.cell = cell
            if assigned_to_uid is not None:
                ticket_instance.assigned_to_uid = assigned_to_uid
            key: Optional[ndb.Key] = ticket_instance.put()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def update_ticket_async(self, ticket_id: Optional[str], topic: Optional[str] = None,
                                  subject: Optional[str] = None, message: Optional[str] = None,
                                  email: str = Optional[str], cell: Optional[str] = None,
                                  assigned_to_uid: Optional[str] = None) -> tuple:

        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):
            if topic is not None:
                ticket_instance.topic = topic
            if subject is not None:
                ticket_instance.subject = subject
            if message is not None:
                ticket_instance.message = message
            if email is not None:
                ticket_instance.email = email
            if cell is not None:
                ticket_instance.cell = cell
            if assigned_to_uid is not None:
                ticket_instance.assigned_to_uid = assigned_to_uid
            key: Optional[ndb.Key] = ticket_instance.put_async().get_result()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def assign_ticket(self, ticket_id: str, assigned_to_uid: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):

            ticket_instance.assigned_to_uid = assigned_to_uid
            key: Optional[ndb.Key] = ticket_instance.put()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def assign_ticket_async(self, ticket_id: str, assigned_to_uid: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):

            ticket_instance.assigned_to_uid = assigned_to_uid
            key: Optional[ndb.Key] = ticket_instance.put_async().get_result()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def send_response_by_email(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send email response mark ticket save ticket save response
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):
            ticket_instance.response_sent = True
            key: Optional[ndb.Key] = ticket_instance.put()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # Note: scheduled response by email
            _kwargs: dict = dict(ticket_id=ticket_id, subject=subject, message=message)
            _job_name: str = self._create_job_name(header_name='ticket_send_response_by_mail_')
            self._base_email_scheduler(func=self._send_ticket_response, kwargs=_kwargs, job_name=_job_name)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def send_response_by_email_async(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send email response mark ticket save ticket save response
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):

            ticket_instance.response_sent = True
            key: Optional[ndb.Key] = ticket_instance.put_async().get_result()
            # TODO Send response here
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # Note: scheduled response by email
            _kwargs: dict = dict(ticket_id=ticket_id, subject=subject, message=message)
            _job_name: str = self._create_job_name(header_name='tickets_sms_notification_')
            self._base_email_scheduler(func=self._send_ticket_response, kwargs=_kwargs, job_name=_job_name)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def send_sms_notification(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send notification update ticket to reflect that notification was sent
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):

            ticket_instance.response_sent = True
            key: Optional[ndb.Key] = ticket_instance.put()
            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)
            # Note: scheduled sms notifications
            _kwargs: dict = dict(ticket_id=ticket_id, subject=subject, message=message)
            _job_name: str = self._create_job_name(header_name='send_sms_notification_')
            self._base_email_scheduler(func=self._send_sms_notifications, kwargs=_kwargs, job_name=_job_name)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def send_sms_notification_async(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send notification update ticket to reflect that notification was sent
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):

            ticket_instance.response_sent = True
            key: Optional[ndb.Key] = ticket_instance.put_async().get_result()

            if not bool(key):
                message: str = "Database Error: Unable to update ticket"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # Note: scheduled sms notifications
            _kwargs: dict = dict(ticket_id=ticket_id, subject=subject, message=message)
            _job_name: str = self._create_job_name(header_name='send_sms_notification_')
            self._base_email_scheduler(func=self._send_sms_notifications, kwargs=_kwargs, job_name=_job_name)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def add_response(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket add response
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):

            ticket_instance.response_sent = True
            key: Optional[ndb.Key] = ticket_instance.put()

            if not bool(key):
                message: str = "Database Error: While creating ticket - Ticket not saved"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # Note: scheduled sending ticket response by email
            _kwargs: dict = dict(ticket_id=ticket_id, subject=subject, message=message)
            _job_name: str = self._create_job_name(header_name='send_ticket_response_email_')
            self._base_email_scheduler(func=self._send_ticket_response, kwargs=_kwargs, job_name=_job_name)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code

        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    async def add_response_async(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket add response
        """
        ticket_instance: Ticket = Ticket.query(
            Ticket.ticket_id == ticket_id).get_async().get_result()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):

            ticket_instance.response_sent = True
            key: Optional[ndb.Key] = ticket_instance.put_async().get_result()

            if not bool(key):
                message: str = "Database Error: While creating ticket - Ticket not saved"
                raise DataServiceError(status=error_codes.data_service_error_code, description=message)

            # Note: scheduled sending ticket response by email
            _kwargs: dict = dict(ticket_id=ticket_id, subject=subject, message=message)
            _job_name: str = self._create_job_name(header_name='send_ticket_response_email_')
            self._base_email_scheduler(func=self._send_ticket_response, kwargs=_kwargs, job_name=_job_name)

            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), status_codes.successfully_updated_code
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), status_codes.data_not_found_code

    @use_context
    @handle_view_errors
    def get_all_tickets(self) -> tuple:
        tickets_list: List[dict] = [ticket.to_dict() for ticket in Ticket.query().fetch()]

        if isinstance(tickets_list, list) and tickets_list:
            return jsonify({'status': True, 'payload': tickets_list,
                            'message': 'successfully returned tickets'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate tickets"
        return jsonify({'status': False, 'message': message})

    @use_context
    @handle_view_errors
    async def get_all_tickets_async(self) -> tuple:
        tickets_list: List[dict] = [ticket.to_dict() for ticket in Ticket.query().fetch_async().get_result()]

        if isinstance(tickets_list, list) and tickets_list:
            return jsonify({'status': True, 'payload': tickets_list,
                            'message': 'successfully returned tickets'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate tickets"
        return jsonify({'status': False, 'message': message})

    @use_context
    @handle_view_errors
    def get_unresolved_tickets(self) -> tuple:
        tickets_list: List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == False).fetch()]

        if isinstance(tickets_list, list) and tickets_list:
            return jsonify({'status': True, 'payload': tickets_list,
                            'message': 'successfully returned tickets'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate tickets"
        return jsonify({'status': False, 'message': message})

    @use_context
    @handle_view_errors
    async def get_unresolved_tickets_async(self) -> tuple:
        tickets_list: List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == False).fetch_async().get_result()]

        if isinstance(tickets_list, list) and tickets_list:
            return jsonify({'status': True, 'payload': tickets_list,
                            'message': 'successfully returned tickets'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate tickets"
        return jsonify({'status': False, 'message': message})

    @use_context
    @handle_view_errors
    def get_resolved_tickets(self) -> tuple:
        tickets_list: List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == True).fetch()]

        if isinstance(tickets_list, list) and tickets_list:
            return jsonify({'status': True, 'payload': tickets_list,
                            'message': 'successfully returned tickets'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate tickets"
        return jsonify({'status': False, 'message': message})

    @use_context
    @handle_view_errors
    async def get_resolved_tickets_async(self) -> tuple:
        tickets_list: List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == True).fetch_async().get_result()]

        if isinstance(tickets_list, list) and tickets_list:
            return jsonify({'status': True, 'payload': tickets_list,
                            'message': 'successfully returned tickets'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate tickets"
        return jsonify({'status': False, 'message': message})

    @use_context
    @handle_view_errors
    def fetch_ticket(self, ticket_id: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully returned ticket'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate ticket"
        return jsonify({'status': False, 'message': message})

    @use_context
    @handle_view_errors
    async def fetch_ticket_async(self, ticket_id: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()

        if isinstance(ticket_instance, Ticket) and bool(ticket_instance):
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully returned ticket'}), status_codes.status_ok_code

        message: str = "Data not Found: Unable to locate ticket"
        return jsonify({'status': False, 'message': message})


class TicketThreadView(Validators):
    pass
