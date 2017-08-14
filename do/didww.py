from flask import Blueprint, request
from functools import partial

# DIDWW is a service that supplies DID endpoints for many countries
# They are the only Australian provider of numbers which support
# both Voice and SMS (Aug 2017)

#smsin_bp = Blueprint('smsin', 'DO.DIDWW.SmsIn')
smsin_bp = Blueprint('smsin', __name__)

class SmsIn:
    def __init__(self, to_num, send_obj):
        self.to_num = to_num
        self.send_obj = send_obj

        # Can call twice?
        wrapped = partial(SmsIn.sms_in, self)
        smsin_bp.add_url_rule('/', "sms_in", wrapped, methods=['POST'])

    @staticmethod
    def blueprint():
        return smsin_bp

    #@smsin_bp.route('/', methods=['POST'])
    def sms_in(self):
        # DID post request is custom defined, and not escaped
        # To avoid injection attacks we use the following scheme
        # Headers
        #   SMS-Source       - 61402123123
        #   SMS-Destination  - 61405321321
        #   SMS-Time         - RFC-2822 format
        # Body
        #   sent sms text, in raw unescaped format

        # can parse time with:
        # email.utils.parsedate_tz(string)
        # or
        # email.utils.parsedate_to_datetime(date) 

        body = request.get_data().decode('utf-8').strip()

        if body.startswith(":"):
            _process_command(body)

        out = '{} : {} : {} : {}'.format(
                request.headers.get("SMS-Source"),
                request.headers.get("SMS-Destination"),
                request.headers.get("SMS-Time"),
                request.get_data().decode('utf-8')
        )

        #return Response(str(request.headers), mimetype="text/xml")

        #self.send_obj.send(self.to_num, out)
        self.send_obj.send(self.to_num, '+12563049271', str(request.headers))

        return ('', 204)



