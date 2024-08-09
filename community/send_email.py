from django.core.mail import EmailMessage
from .models import Community, Information

def send_email_to_multiple_recipients():
    # subject = 

    email = EmailMessage(
        'Hello',
        'Body goes here',
        'from@example.com',
        ['first@example.com', 'second@example.com'],
        ['bcc@example.com'],
        reply_to=['another@example.com'],
        headers={'Message-ID': 'foo'},
    )

# email.send()