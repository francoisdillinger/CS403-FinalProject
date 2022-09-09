# CS403-FinalProject

### This project was completed during CS403-Cloud Computing. It utilizes the following AWS services:

    1. EC2
    2. RDS
    3. SES
    4. S3
    5. Lambda
 
## Project Details:
Unfortunately, this project is not live as allocating and running AWS services isn't free and occasionally allocating resources would require generating all new access codes and keys for the majority of services. The other issue is that the project is using SES to send email notifications, but utilizing SES initially results in users being placed in a sandbox by Amazon to prevent abuse of the services being used for spamming. As such, the only way out of the sandbox is to apply for a production version which didn't seem worth it for a project.

This project was to have the following functionality:

    1. Have a registration/login screen.
    2. Once a user is logged in, they are presented with a submission form to submit a file and up to 5 email addresses.
    3. Once submitted, the file is uloaded to S3, and an SES notification is sent to each email the user entired.
    3. A copy of the file name and logged in user is saved in a database for later billing purposes.
    4. Project must be run in an EC2 instance.
    
How project was made and which AWS services were implemented:

    1. Project was built with Python, Flask, Bootstrap, and SQLAlchemy.
    2. Project was hosted on an AWS-EC2 instance.
    3. During registration, user account was created and saved in AWS-RDS.
    4. When user uploads a file and up to 5 email address, the file is uploaded to AWS-S3 and emails are saved in AWS-RDS.
    5. When file is loaded in AWS-S3, AWS-Lambda is triggered and reads the recipient emails from AWS-RDS and sends a 
       presigned URL to each recipient email with AWS-SES.
       
Since this isn't a project others can test for themselves, I have uploaded a video which shows the working functionality of the project as well as the AWS services that were used. For the presentation video of this project, please click [here](https://www.youtube.com/watch?v=kLHzBDySR3o).
