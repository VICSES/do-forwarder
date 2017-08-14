import boto3
from config import aws_access_key_id, aws_secret_access_key


# Store a file using S3
# For example a static twilio redirect

class S3:


    def store_xml(bucket, filename, content):
        # Set twilio redirect using S3 stored twiml file
        aws = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
        s3 = aws.resource('s3')


        # Considered adopting a upload, copy, delete pattern
        # However Amazon promises that the upload is atomic
        # Failures and partial uploads don't propogate and can't be fetched

        up_ret = s3.Object(bucket, filename).put(
                Body=content.encode(),
                ContentEncoding='text/xml',
                ACL='public-read'
        )

        # It seems most errors cause s3.Object to throw execptions
        # Check the returned object just to be sure
        if 'ETag' not in up_ret:
            raise Exception()
        if up_ret.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
            raise Exception()
