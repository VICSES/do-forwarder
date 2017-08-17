from flask import Blueprint, request
from email.utils import parsedate_to_datetime
from functools import partial

# DIDWW is a service that supplies DID endpoints for many countries
# They are the only Australian provider of numbers which support
# both Voice and SMS (Aug 2017)

class SmsIn:
    def __init__(self, recv_callback):
        if not callable(recv_callback):
            raise TypeError("recv_callback must be callable")
        self.recv_callback = recv_callback
        self.smsin_bp = Blueprint('smsin', __name__)


        # Can call twice?
        wrapped = partial(SmsIn.sms_in, self)
        self.smsin_bp.add_url_rule('/', "sms_in", wrapped, methods=['POST'])

    def blueprint(self):
        return self.smsin_bp

    def sms_in(self):
        # DID post request is custom defined, and not escaped
        # To avoid injection attacks we use the following scheme
        # Headers
        #   SMS-Source       - 61402123123
        #   SMS-Destination  - 61405321321 (our number)
        #   SMS-Time         - RFC-2822 format
        # Body
        #   sent sms text, in raw unescaped format

        body = request.get_data().decode('utf-8')
        to_num = request.headers.get("SMS-Destination")
        from_num = request.headers.get("SMS-Source")
        time = parsedate_to_datetime(request.headers.get("SMS-Time"))

        self.recv_callback(from_num, to_num, body, time)

        return ('', 204)
