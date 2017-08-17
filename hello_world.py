from flask import Flask, request, Response
from twilio.rest import Client

from config import twilio_account_sid, twilio_auth_token
from config import aws_access_key_id, aws_secret_access_key

import re


class DoManager:
    def __init__(self, voip_ctrl = None, sms_in = None, sms_out = None):
        # Due to different possible configurations the do_manager
        # must be passed three objects, classes or functions to
        # provide the required functionality
        #
        # voip_ctrl - controls the voice call redirection
        #           - must provide set_redirect()
        # sms_in    - provides a facility to capture incoming SMS
        #           - it may provide a function called capture, or use init
        # sms_out   - provides a facility to send SMS
        #           - must provide send_sms()

        if inspect.isclass(voip_ctrl):
            self.voip_ctrl = voip_ctrl()
        else:
            self.voip_ctrl = voip_ctrl
        try:
            self.set_redirect = self.voip_ctrl.set_redirect
        except AttributeError:
            if inspect.isfunction(self.voip_ctrl):
                self.set_redirect = self.voip_ctrl
            else:
                self.set_redirect = None

        if inspect.isclass(sms_in):
            self.sms_in = sms_in()
        else:
            self.sms_in = sms_in
        try:
            self.capture = self.sms_in.capture()
        except AttributeError:
            if inspect.isfunction(self.sms_in):
                self.capture = self.sms_in()
            else:
                self.capture = self.sms_in

        if inspect.isclass(sms_out):
            self.sms_out = sms_out()
        else:
            self.sms_out = sms_out
        try:
            self.send_sms = self.sms_out.send_sms
        except AttributeError:
            if inspect.isfunction(self.sms_out):
                self.send_sms = self.sms_out
            else:
                self.send_sms = None


# We only need this for local development.
if __name__ == '__main__':
    app.run()
