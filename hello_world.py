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


    class Twilio:
        # Provides voip_ctrl, sms_in and sms_out
        def __init__(self):
            self.app = Flask(__name__)

            self.app.add_url_rule('/sms', view_func=DoTwilio._sms_in, methods=['POST']

        def _sms_in():
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
            #
            # Returning Twiml Response to send on message
            
            to = '+61439069336'
            x  = '<?xml version="1.0" encoding="UTF-8"?>'
            x += '<Response>'
            x += '<Message to="{}">'.format(to)
            x += "From: {}\n".format(request.form.get("From"))
            x += request.form.get("Body", "empty sms")
            x += '</Message>'
            x += '</Response>'

            return Response(x, mimetype='text/xml')

        tclient = Client(twilio_account_sid, twilio_auth_token)

        def send_sms(to, body, frm = '+12563049271'):
            # frm == from, from is a reserved word

            message = tclient.messages.create(
                    body=body,
                    to=to,
                    from_=frm)

            # TODO: Should do something with the response, especially if it is bad

        def set_redirect(num)
            # Set twilio redirect using S3 stored twiml file
            aws = boto3.Session(
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)
            s3 = aws.resource('s3')


            # Considered adopting a upload, copy, delete pattern
            # However Amazon promises that the upload is atomic
            # Failures and partial uploads don't propogate and can't be fetched

            up_ret = s3.Object(bucket, target_key).put(
                    Body=_gen_redirect(target_number).encode(),
                    ContentEncoding='text/xml',
                    ACL='public-read'
            )

            # It seems most errors cause s3.Object to throw execptions
            # Check the returned object just to be sure
            if 'ETag' not in up_ret:
                raise Exception()
            if up_ret.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
                print(str(up_ret))
                print(up_ret.get('HTTPStatusCode'))
                print(up_ret.get('HTTPStatusCode') != 200)
                raise Exception()



        def _gen_redirect(target_number):
            target_number = re.sub(r"\D", "", target_number)
            if target_number.startswith('614') and target_number.len() == 11:
                return (''
                    + '<?xml version="1.0" encoding="UTF-8"?>'
                    + '<Response>'
                    +     '<Dial>'
                    +         '<Number>+{}</Number>'
                    +     '</Dial>'
                    + '</Response>').format(target_number);
            else:
                pass # TODO: Error return



        
def _cmd_transfer(args):
    # :transfer <phone number>
    # :transfer <name>

    if re.search('[a-zA-Z]', args):
        # Any alpha characters -> name
        pass # TODO - map names
    else:
        # No alpha characters -> number
        num = re.sub(r"\D", "", args)

        # Must be a sane Australian mobile number
        # Can be either local or international format
        # Must output international format
        if num.startswith("04") and num.len() == 10:
            num = '61' + num[1:]

        if num.startswith('614') and num.len() == 11:
            _set_redirect(num)
        else:
            pass # TODO: bad number format

def _process_command(cmd):
    cmd = cmd.lstrip(' :')

    #processor = getattr(self, '_cmd_'+cmd.split(' ',1)[0].lower(), None)
    processor_name = '_cmd_{}'.format(cmd.split(' ',1)[0].lower())

    try:
        locals()[processor_name](cmd.split(' ',1)[1])
    except KeyError:
        pass # TODO


    


@app.route('/didwwsms', methods=['POST'])
def didwwsms():
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

    _send_sms('+61439069336', out)
    #_send_sms('+61439069336', str(request.headers))

    return ('', 204)


@app.route('/sms', methods=['POST'])
def sms():
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
    #
    # Returning Twiml Response to send on message
    
    to = '+61439069336'
    x  = '<?xml version="1.0" encoding="UTF-8"?>'
    x += '<Response>'
    x += '<Message to="{}">'.format(to)
    x += "From: {}\n".format(request.form.get("From"))
    x += request.form.get("Body", "empty sms")
    x += '</Message>'
    x += '</Response>'

    return Response(x, mimetype='text/xml')


 
# We only need this for local development.
if __name__ == '__main__':
    app.run()
