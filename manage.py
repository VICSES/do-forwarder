from flask import Flask

from do.didww import SmsIn
from do.twilio import SmsOut


sms_out = SmsOut()
sms_in = SmsIn('+61439069336', sms_out)


app = Flask(__name__)
app.register_blueprint(sms_in.blueprint(), url_prefix='/sms')
