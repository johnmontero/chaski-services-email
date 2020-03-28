import json
import uuid
from datetime  import datetime
from chalicelib.utils.db import get_item
from chalicelib.utils.db import put_item
from chalicelib.utils.db import update_item
from chalicelib.utils.constants import PENDING_STATE
from chalicelib.utils.constants import HTTP_OK
from chalicelib.utils.format import format_strdate_to_cmpdate
from chalicelib.utils.exceptions import ExceptionHandler
from chalicelib.utils.mail import create_mail_html
from chalicelib.utils.mail import build_msg_to_mail
from chalicelib.utils.mail import send_mail

from chalicelib.schemas.message import MessageSchema

class MessageResource(object):

    def __init__(self, config, app):
        self.config = config
        self.app = app
        self.table_name_message = self.config.get('TABLE_NAME_MESSAGE')

    def _validate_payload(self, payload):
        errors = MessageSchema().validate(payload)
        if len(errors) > 0:
            raise ExceptionHandler(json.dumps(errors))
    
    def _prepared_data_message(self, payload):
        payload.update({
            'id': '{}'.format(str(uuid.uuid4())),               
            'create_at': str(datetime.now()),
            'update_at': str(datetime.now()),
            'state': PENDING_STATE
        })
        return payload

    def _save_data_message(self, data):
        pass

    def _prepare_data_context_html(self, data):     
        data_context = data.get('metadata')
        return data_context

    def _send_message(self, payload):
        email_from = "{} <{}>".format(
            payload.get('from').get('name'),
            payload.get('from').get('email'),
        )
        subject = payload.get("subject")
        data_context_html = self._prepare_data_context_html(payload)
        for to in payload.get("to"):
            emails_to = [
                "{} <{}>".format(to.get('name'), to.get('email'))
            ]
            email_html = create_mail_html('message.html', data_context_html)
            msg = build_msg_to_mail(
                email_from, 
                emails_to, 
                subject,
                email_html
            )
            response = send_mail(email_from, emails_to, msg)

    def on_post(self, request):
        payload = request.json_body
        self._validate_payload(payload)
        data_message = self._prepared_data_message(payload)
        # self._save_data_message(data_message)
        self._send_message(payload)
        response = {
            'code': HTTP_OK,
            'message':f'Message successfully was saved.',
            'data': {
                'id': data_message.get('id'),
                'create_at': data_message.get('create_at'),
                'update_at': data_message.get('update_at'),
                'state': data_message.get('state')
            }
        }
        
        return response