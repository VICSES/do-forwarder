import boto3

bucket = 'belses-redirect'
target_key = 'twiml.xml'


from config import aws_access_key_id, aws_secret_access_key


def gen_redirect_twiml(target_number):
    # TODO: Ensure target_number is the correct format
    return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Dial>
        <Number>+{}</Number>
    </Dial>
</Response>""".format(target_number);


def set_redirect(target_number):
    aws = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)
    s3 = aws.resource('s3')

    # Considered adopting a upload, copy, delete pattern
    # However Amazon promises that the upload is atomic
    # Failures and partial uploads don't propogate and can't be fetched

    up_ret = s3.Object(bucket, target_key).put(
            Body=gen_redirect_twiml(target_number).encode(),
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

set_redirect('04020273211')
