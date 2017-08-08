from flask import Flask, request, Response
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return "Hello, world!", 200

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
