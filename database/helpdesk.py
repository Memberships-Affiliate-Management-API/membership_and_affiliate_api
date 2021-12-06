from datetime import datetime
from typing import Optional

from google.cloud import ndb

from database.basemodel import BaseModel
from database.setters import property_


class HelpDeskValid:
    pass


class HelpDesk(BaseModel):
    help_desk_active: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    total_tickets: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    total_tickets_opened: int = ndb.IntegerProperty(default=0, validator=property_.set_number)
    total_tickets_closed: int = ndb.IntegerProperty(default=0, validator=property_.set_number)

    def __str__(self) -> str:
        """
        :return:
        """
        return f"<HelpDesk total_tickets: {self.total_tickets}, total_open : {self.total_tickets_closed}, " \
               f"total_closed: {self.total_tickets_opened}"

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.total_tickets != other.total_tickets:
            return False
        if self.total_tickets_opened != other.total_tickets_opened:
            return False
        if self.total_tickets_closed != other.total_tickets_closed:
            return False
        return True

    def __bool__(self) -> bool:
        # Cannot use bool as total_tickets of 0 will return False
        # return True if self.total_tickets is not None else False
        return bool(self.help_desk_active)


class TicketValid:
    """
        **Class Ticket Validators**
            useful methods for tickets validations
    """

    @staticmethod
    def is_topic_valid(topic: Optional[str]) -> bool:
        if not isinstance(topic, str) or not bool(topic.strip()):
            return False
        return True

    @staticmethod
    def is_subject_valid(subject: Optional[str]) -> bool:
        if not isinstance(subject, str) or not bool(subject.strip()):
            return False
        return True

    @staticmethod
    def is_message_valid(message: Optional[str]) -> bool:
        if not isinstance(message, str) or not bool(message.strip()):
            return False
        return True


class Ticket(BaseModel):
    """
    **Class Ticket**
        a class to keep track of every ticket detail which is opened

    """
    ticket_id: str = ndb.StringProperty(indexed=True, required=True, validator=property_.set_id)
    uid: str = ndb.StringProperty(indexed=True, required=True, validator=property_.set_id)
    topic: str = ndb.StringProperty(indexed=True, required=True, validator=property_.set_string)
    subject: str = ndb.StringProperty(indexed=True, required=True, validator=property_.set_string)
    message: str = ndb.StringProperty(required=True, validator=property_.set_string)
    email: str = ndb.StringProperty(required=True, validator=property_.set_email)
    cell: str = ndb.StringProperty(validator=property_.set_cell)
    assigned: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    assigned_to_uid: str = ndb.StringProperty(validator=property_.set_id)
    response_sent: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    is_resolved: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    client_not_responding: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    time_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.ticket_id != other.ticket_id:
            return False
        if self.uid != other.uid:
            return False
        if self.topic != other.topic:
            return False
        return True

    def __str__(self) -> str:
        """
        self.topic, self.subject, self.message, self.email, self.cell, self.is_resolved
        :return:
        """
        return f"<Ticket topic: {self.topic}, subject: {self.subject}, message: {self.message}, email: {self.email}, " \
               f"cell: {self.cell}, is_resolved: {self.is_resolved}"

    def __bool__(self) -> bool:
        return bool(self.ticket_id) and bool(self.uid)
        # return True if self.ticket_id or self.uid else False


class TicketThreadValid:
    """
        Error checking for ticket thread
    """
    pass


class TicketThread(BaseModel):
    """
    **Class TicketThread**
        keeps track of each ticket threads for easy loading on user interfaces

    **Note**
        sort by ticket_id, then time_created , then mark by sent_by to create thread
    """
    ticket_id: str = ndb.StringProperty(indexed=True, required=True, validator=property_.set_id)
    thread_id: str = ndb.StringProperty(indexed=True, required=True, validator=property_.set_id)
    user_type: str = ndb.StringProperty(validator=property_.set_user_type)  # Support Staff or Client
    subject: str = ndb.StringProperty(validator=property_.set_string)
    message: str = ndb.StringProperty(validator=property_.set_string)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    time_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)

    # noinspection DuplicatedCode
    def __eq__(self, other) -> bool:
        if self.__class__ is not other.__class__:
            return False
        if self.ticket_id != other.ticket_id:
            return False
        if self.thread_id != other.thread_id:
            return False
        if self.sent_by != other.sent_by:
            return False
        if self.time_created != other.time_created:
            return False
        return True

    def __str__(self) -> str:
        """
        :return: str representation of TicketThread
        """
        return f"<TicketThread Sent_by: {self.sent_by}, Subject: {self.subject}, Message {self.message} " \
               f"Time_Created: {self.time_created}"

    def __bool__(self) -> bool:
        return bool(self.ticket_id) and bool(self.thread_id)
        # return True if self.ticket_id else False
