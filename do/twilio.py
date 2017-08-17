from twilio.rest import Client
from flask import Blueprint, request
from config import twilio_account_sid, twilio_auth_token

client = Client(twilio_account_sid, twilio_auth_token)

#voipctrl_bp = Blueprint('voipctrl', __name__+'.VoipCtrl')
voipctrl_bp = Blueprint('voipctrl', __name__)

class VoipCtrl:
    @staticmethod
    def blueprint():
        return voipctrl_bp

    def __init__(self, to_num):
        self.to_num = to_num

    def gen_redirect(self, target_num = None):
        if target_num == None:
            target_num = self.to_num

        target_num = re.sub(r"\D", "", target_num)
        if target_num.startswith('614') and target_num.len() == 11:
            return (''
                + '<?xml version="1.0" encoding="UTF-8"?>'
                + '<Response>'
                +     '<Dial>'
                +         '<Number>+{}</Number>'
                +     '</Dial>'
                + '</Response>').format(target_num);
        else:
            pass # TODO: Error return

    @voipctrl_bp.route('/', methods=['POST'])
    def redirect_in():
        # Incoming call from twilio
        # Will pass details of call, documented somewhere
        twiml = self.gen_redirect()
        return Response(twiml, mimetype='text/xml')


#smsin_bp = Blueprint('smsin', 'DO.Twilio.SmsIn')
smsin_bp = Blueprint('smsin', __name__)

class SmsIn:
    # send_obj is optional, must have a send() method if supplied
    # if not supplied a twiml object is returned to forward the sms
    def __init__(self, to_num, send_obj=None):
        self.to_num = to_num
        self.send_obj = send_obj

    @staticmethod
    def blueprint():
        return smsin_bp

    @smsin_bp.route('/', methods=['POST'])
    def sms_in():
        # Incoming SMS from twilio
        # Documented at https://www.twilio.com/docs/api/twiml/sms/twilio_request
        # TwiML message has post fields:
        #    MessageSid  
        #    SmsSid  == MessageSid, depreciated
        #    AccountSid  
        #    MessagingServiceSid     
        #    From    
        #    To  
        #    Body    
        #    NumMedia
        #  If NumMedia:
        #    MediaContentType{N}
        #    MediaUrl{N}
        #  Optional:
        #    FromCity    The city of the sender
        #    FromState  
        #    FromZip     
        #    FromCountry     
        #    ToCity
        #    ToState
        #    ToZip   
        #    ToCountry

        to_num = self.to_num
        from_num = request.form.get("From")
        body = request.form.get("Body", "empty sms")

        if self.send_obj:
            self.send_obj.send(to_num, from_num, body)
            return ('', 204) # 204 == No Content
        else:
            twiml = self._gen_twiml(to_num, from_num, body)
            return Response(twiml, mimetype='text/xml')

    @staticmethod
    def _gen_twiml(to_num, from_num, body):
        x  = '<?xml version="1.0" encoding="UTF-8"?>'
        x += '<Response>'
        x += '<Message to="{}">'.format(to_num)
        x += "From: {}\n".format(from_num)
        x += body
        x += '</Message>'
        x += '</Response>'
        return x




class SmsOut:
    @staticmethod
    def send(to_num, from_num, body):
        # NOTE: One SMS is up to 160 GSM characters
        #       Above 160 characters we send a multi-part message
        #       Each multipart message is up to 153 GSM characters
        #       GSM characters are A-Za-z0-9 and a few bonus characters
        #       Different language tables and UTF-16/UCS-2 are supported
        #       UTF-16 allows up to 70 characters per message
        message = client.messages.create(
                body=body,
                to=to_num,
                from_=from_num)

        # TODO: Should do something with the response, especially if it is bad
