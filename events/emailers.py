from _sdk._email import Mailgun


class EmailerEvents(Mailgun):

    def __init__(self):
        super(EmailerEvents, self).__init__()
        self._event_queue: list = []
