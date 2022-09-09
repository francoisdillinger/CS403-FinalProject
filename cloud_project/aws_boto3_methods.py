import boto3
import json
import logging
import botocore
from botocore.exceptions import ClientError
from botocore.client import Config

def aws_ses(email):
    # boto3 client being passed (aws-service, aws_access_key_id, aws_secret_access_key)
    client = boto3.client('ses', aws_access_key_id='', aws_secret_access_key='')
    
    # calling ses client method to send and verify email address
    client.verify_email_identity(EmailAddress=email)
    

def aws_s3_upload(local_file, s3_filename):
    # boto3 client being passed (aws-service, aws_access_key_id, aws_secret_access_key)
    s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
    
    # s3 upload method being passed (local-file, s3-bucket-name, new-s3-file-name)
    s3.upload_file(local_file, 'final-project-bucket-cs403', s3_filename, Callback=print('File transfered.'))

    print(f'File {s3_filename} added to s3 bucket.')


# def aws_s3_delete(s3_filename):
#     # boto3 client being passed (aws-service, aws_access_key_id, aws_secret_access_key)
#     s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')

#     # Prettified response from deleting file from s3 bucket
#     prettyResponse = json.dumps(s3.delete_object(Bucket = 'final-project-bucket-cs403', Key = s3_filename), indent=2)
    
#     # Printing response
#     print(f'Deleting {s3_filename} file from s3 bucket: ')
#     print(prettyResponse)   




# def create_presigned_url(bucket_name, object_name, expiration=600):
#     # Used following url to resolve authorization issue
#     # https://stackoverflow.com/questions/26533245/the-authorization-mechanism-you-have-provided-is-not-supported-please-use-aws4   
#     # Generate a presigned URL for the S3 object
#     s3 = boto3.client('s3',config=Config(signature_version='s3v4'),region_name='us-east-2',aws_access_key_id='', aws_secret_access_key='')
#     try:
#         response = s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
#     except Exception as e:
#         print(e)
#         logging.error(e)
#         return "Error"
#     # The response contains the presigned URL
#     return response


