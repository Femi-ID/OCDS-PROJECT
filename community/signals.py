from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import User
from .models import Community, Information
from django.core.mail import EmailMessage

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail

# setup port number and server name
smtp_port = settings.EMAIL_PORT
smtp_server = settings.EMAIL_HOST
email_from = settings.EMAIL_HOST_USER
password = settings.EMAIL_HOST_PASSWORD
# subject = 'New email from OCDS community:' # change to instance.title

sender_mail = "from@example.com"

# print(user)

@receiver(post_save, sender=Information)
def post_save_send_email(sender, instance, created, **kwargs):
    users = User.objects.filter(community='0de864b8-8b6f-4186-9358-6506bbe8e9ea')
    email_list = []
    for member in users:
        email_list.append(member.email)

    if created:
        subject = instance.title
        msg = instance.content
        
        message1 = (
        subject,
        msg,
        email_from,
        email_list,
        # [x for x in users if users.email is not None],
        # ['technewmann@gmail.com', 'workboy238@gmail.com'],
        ),
        
        print(users)
        # print('email_list: ', email_list)
        send_mass_mail(message1, fail_silently=False)
        print(f'Email sent...congrats')


        # community_members = User.objects.filter(community__name='ocds-general-community')
        # context = ssl.create_default_context()
        # email_list = []
        # for member in community_members:
        #     email_list.append(member.email)
        # try:
        #     # def send_emails(email_list):
        #     for member in email_list:
        #         # Make the body of the email:
        #         body = str(instance.content)

        #         # Make a MIME object to define small parts of the email:
        #         msg = MIMEMultipart()
        #         msg['From'] = email_from
        #         msg['To'] = member
        #         msg['Subject'] = subject

        #         # Attach the body of the message
        #         msg.attach(MIMEText(body, 'plain'))

        #         # Cast as string
        #         text = msg.as_string()

        #         # Connect with the server
        #         print("Connecting to server...")
        #         TIE_server = smtplib.SMTP(smtp_server, smtp_port) # server & port as arguments
        #         TIE_server.starttls(context=context)
        #         TIE_server.login(email_from, password)
        #         print('Successfully connected to server')

        #         # Send email to the list provided
        #         print(f'Sending email to {email_list}')
        #         TIE_server.sendmail(email_from, email_list, text)
        #         print(f'Email sent...congrats')
        # except Exception as e:
        #     print(e)
        # finally:
        #     TIE_server.quit()

            # send_emails(community_members)



# message1 = (
#   "Subject here",
#   "Here is the message",
#   sender_mail,
#   [x for x in user if user.email is not null],
# )