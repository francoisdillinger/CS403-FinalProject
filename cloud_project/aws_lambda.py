  # Importing necessary modules
import pymysql
import boto3
import json
import logging
from botocore.client import Config

# Access key variables
ACCESS_KEY_ID = ''
SECRET_ACCESS_KEY = ''
REGION_NAME = 'us-east-2'

def send_ses(emails, url):
    # Creating a formatted string for the email
    message = f'Here is the newest s3 bucket upload: <a class="ulink" href="{url}" target="_blank">Open this safe file</a>.'

    # Sending the email with ses
    client = boto3.client('ses', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY, region_name=REGION_NAME)
    response = client.send_email(
        Destination={'ToAddresses': emails},
        Message={
            'Subject': {'Data': 'A new file has been uploaded.','Charset': 'UTF-8'},
            'Body': {'Html': {'Data': message,'Charset': 'UTF-8'}}
        },
        ReplyToAddresses=['@gmail.com'],
        Source='@gmail.com',
        SourceArn='',
        ReturnPathArn='',
    )


# Used following url to resolve authorization issue
# https://stackoverflow.com/questions/26533245/the-authorization-mechanism-you-have-provided-is-not-supported-please-use-aws4  
def create_presigned_url(bucket_name, object_name, expiration=600):
    # Generating and returning a presigned url from s3
    s3 = boto3.client('s3',config=Config(signature_version='s3v4'),region_name=REGION_NAME,aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    response = s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
    return response
    
def lambda_handler(event, context):
    # Conneting to DB and getting emails from file upload
    connection = pymysql.connect(host='database-url',user='',password='',database='',cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute('''SHOW DATABASES''')
    cursor.execute('''use users''')
    cursor.execute('''SELECT * from recipients''')
    
    # Creating a list of emails to be used with ses
    emails = []
    for email in cursor:
        emails.append(email['email'])
    
    # Getting the file, creating a presigned url, and sending the link with ses
    bucket = event['Records'][0]['s3']['bucket']['name']
    file = event['Records'][0]['s3']['object']['key']
    url = create_presigned_url(bucket, file)
    send_ses(emails, url)