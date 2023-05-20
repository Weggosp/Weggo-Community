from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os
my_api_key = os.environ.get('SENDGRID_API_KEY')

from flask import render_template
class Sends:
    def common_no_reply(items):
        message = Mail(
            from_email='no-reply@weggo.es',
            to_emails=items['email'],
            subject=items['subject'],
            html_content=render_template(items['template_route'], data=items)
        )
        try:
            sg = SendGridAPIClient(my_api_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    ## TEAM (GENERAL ACCESS TO WORKERS)
    def common_team(items):
        message = Mail(
            from_email='team@weggo.es',
            to_emails=items['email'],
            subject=items['subject'],
            html_content=render_template(items['template_route'], data=items)
        )
        try:
            sg = SendGridAPIClient(my_api_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
