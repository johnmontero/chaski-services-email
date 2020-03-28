import boto3
from botocore.exceptions import ClientError

from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from .exceptions import ExceptionHandler

from .render import render_template
from .render import templates_dir

ses = boto3.client('ses')

def create_mail_html(name, data):
    context = {'data': data }
    return render_template(templates_dir, name, **context)

def build_msg_to_mail(email_from, emails_to, subject, email_html):

    msg = MIMEMultipart('alternative')
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = COMMASPACE.join(emails_to)
    
    part_text = MIMEText(email_html, 'plain')
    part_html = MIMEText(email_html, 'html')
    msg.attach(part_text)
    msg.attach(part_html)

    return msg

def send_mail(email_from, emails_to, msg):
    try:
        response = ses.send_raw_email(
            Source=email_from,
            Destinations=emails_to,
            RawMessage={
                'Data': msg.as_string()
            }
        )
    except ClientError as e:
        raise ExceptionHandler(e.response['Error']['Message'])

    return response
