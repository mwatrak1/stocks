import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
my_number = '+12098503548'


def send_whatsapp_message(message_content, receiver):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_content,
        from_=my_number,
        to=receiver
    )
