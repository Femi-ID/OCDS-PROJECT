# from django.core.mail import EmailMessage
# from .models import Community, Information

# def send_email_to_multiple_recipients():
#     # subject = 

#     email = EmailMessage(
#         'Hello',
#         'Body goes here',
#         'from@example.com',
#         ['first@example.com', 'second@example.com'],
#         ['bcc@example.com'],
#         reply_to=['another@example.com'],
#         headers={'Message-ID': 'foo'},
#     )

# email.send()


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings

# setup port number and server name
smtp_port = settings.EMAIL_PORT
# smtp_port = 587
smtp_server = settings.EMAIL_HOST
# smtp_server = 'smtp.gmail.com'
email_from = settings.EMAIL_HOST_USER
# email_from = 'technewmann@gmail.com'
email_list = ['femipaul33@yahoo.com', 'femiidowu28@gmail.com']
password = settings.EMAIL_HOST_PASSWORD
# password = 'rlemzpuplohwhdog'
# message = 'Message displayed here'
subject = 'New email from OCDS community.'

def send_emails(email_list):
    for email in email_list:
        # Make the body of the email:
        body = """
        Email body goes here.
        Let's learn how to manipulate the input/message sent from the admin user.
        To be formatted on every full-stop or keep source formatting design.
        """

        # Make a MIME object to define small parts of the email:
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach:
        filename = 'transactions.xlsx'

        # Open the in base
        attachment = open(filename, 'rb') # r- read, b- binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', 'attachment; filename= '  + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port) # server & port as arguments
        TIE_server.starttls()
        TIE_server.login(email_from, password)
        print('Successfully connected to server')

        # Send email to the list provided
        print(f'Sending email to {email_list[:20]}')
        TIE_server.sendmail(email_from, email_list, text)
        print(f'Email sent...congrats')
    TIE_server.quit()

send_emails(email_list)