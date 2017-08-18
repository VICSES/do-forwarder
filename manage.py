from flask import Flask

from do.didww import SmsIn
#from do.twilio import SmsOut
from do.stubs import SmsOut
from do.command_parser import CommandParser

our_num = '61488805509'
target_phone = '61439069336'

class ManageCmd(CommandParser):
    def _set_redirect(self, num):
        global target_phone
        target_phone = num

    def _get_redirect(self):
        return target_phone

    def _notify(self, num, text):
        sms_out.send(num, our_num, text)


def recv_sms(from_num, to_num, body, time):
    if cmd_parser.is_cmd(body):
        msg = cmd_parser.process_command(from_num, to_num, body, time)
        sms_out.send(from_num, to_num, msg)
    else:
        msg = "From: {}\n{}".format(from_num, body)
        sms_out.send(target_phone, to_num, msg)


cmd_parser = ManageCmd()
sms_out = SmsOut()
sms_in = SmsIn(recv_sms)


app = Flask(__name__)
app.register_blueprint(sms_in.blueprint(), url_prefix='/sms')
