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
from typing import List


class Mailgun:
    def __init__(self):
        ***REMOVED***
            mailgun_domain : domain name registered with mailgun
            MAILGUN_API_KEY : can be found from mailgun control panel
        ***REMOVED***
        self.api = config_instance.MAILGUN_API_KEY
        self.end_point = "https://api.mailgun.net/v3/{}/messages".format(config_instance.MAILGUN_DOMAIN)
        self.no_response = config_instance.MAILGUN_NO_RESPONSE
        self._admin_get_user_endpoint = '_api/admin/users/get'

    def __get_user_data(self, organization_id: str, uid: str) -> any:
        ***REMOVED***
            from an api obtain user details related to the parameters
        :param organization_id: organization_id related to the user
        :param uid: uid of the user
        :return:
        ***REMOVED***
        _url: str = "{}{}".format(config_instance.BASE_URL, self._admin_get_user_endpoint)
        json_data = jsonify({'organization_id': organization_id, 'uid': uid})
        response, status = requests.post(url=_url, json=json_data)
        json_data = response.json()
        if json_data.get('status'):
            user_data: dict = json_data.get('payload')
            return user_data
        return None

    def __send_with_mailgun_rest_api(self, to_list: List[str], subject: str, text: str, html: str,
                                     o_tag: List[str] = None) -> tuple:
        ***REMOVED***
        a method to send email via rest api
        :param o_tag:  message o tag | format of o:tag  ["September newsletter", "newsletters"]
        :param to_list: list of email addresses to send this email format ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"]
        :param subject: the subject of the email
        :param text: the text part of the email
        :param html: the html part of the email
        :return: tuple indicating the status of the message sent
        ***REMOVED***
        # NOTE: from mail must be registered with MAILGUN
        from_str = "{} <{}>".format(config_instance.APP_NAME, self.no_response)
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
