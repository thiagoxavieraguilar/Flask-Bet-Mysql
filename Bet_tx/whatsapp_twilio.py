# twilio.py
from twilio.rest import Client
from dotenv import load_dotenv
import os 

load_dotenv()

account_sid = os.environ.get('TWILIO_API_KEY')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid,auth_token)

def send_message(body:str):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to='whatsapp:+553388659874'
    )

 
 