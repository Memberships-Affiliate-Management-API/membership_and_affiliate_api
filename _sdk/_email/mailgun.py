***REMOVED***
***REMOVED***

***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***

***REMOVED***

***REMOVED***
***REMOVED***

***REMOVED***
import requests
from flask import jsonify

from config import config_instance
from config.exceptions import status_codes, error_codes


class Mailgun:
    def __init__(self, mailgun_domain: str):
        ***REMOVED***
            domain name registered with Mailgun
        :param mailgun_domain:
        ***REMOVED***
        self.api = config_instance.MAILGUN_API_KEY
        self.end_point = "https://api.mailgun.net/v3/{}/messages".format(mailgun_domain)

    def send_with_rest_api(self, from_mail: str, to_list: list, subject: str, text: str, html: str, o_tag: str) -> tuple:
        ***REMOVED***
        a method to send email via rest api
        :param o_tag:  message o tag | format of o:tag  ["September newsletter", "newsletters"]
        :param from_mail: the email i am sending this email from - this email should be registered with MailGun
        :param to_list: list of email addresses to send this email format ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"]
        :param subject: the subject of the email
        :param text: the text part of the email
        :param html: the html part of the email
        :return: tuple indicating the status of the message sent
        ***REMOVED***
        from_str = "{} <{}>".format(config_instance.APP_NAME, from_mail)
        to_str = to_list
        api_instance = ("api", "{}".format(self.api))

        response = requests.post(url=self.end_point,
                                 auth=api_instance,
                                 data={"from": from_str, "to": to_str,
                                       "subject": subject, "text": text, "html": html, "o:tag": o_tag})

        response_data = response.json()
        if response.status_code == 200:
            message: str = 'Successfully sent email'
            return jsonify({"status": True,
                            'message': message, 'payload': response_data.id}), status_codes.status_ok_code

        message: str = 'Unable to send email please try again later'
        return jsonify({"status": False, "message": message}), error_codes.remote_data_error
