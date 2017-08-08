from flask import Flask, request, Response
from twilio.rest import Client

from config import twilio_account_sid, twilio_auth_token
 
app = Flask(__name__)

tclient = Client(twilio_account_sid, twilio_auth_token)

def _send_sms(to, body, frm = '+12563049271'):
    # frm == from, from is a reserved word

    message = tclient.messages.create(
            body=body,
            to=to,
            from_=frm)

    # TODO: Should do something with the response, especially if it is bad
 
@app.route('/')
def index():
    return "Hello, world!", 200

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

    body = request.get_data().decode('utf-8')

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
