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
    # DID post request is custom defined, our is:
    #   src, sms sender
    #   dst, sms receiver
    #   time, received time
    #   body, received message

    out = '{} : {} : {} : {}'.format(
            request.form.get("src"),
            request.form.get("dst"),
            request.form.get("time"),
            request.form.get("body"),
    )

    _send_sms('+61439069336', out)

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
