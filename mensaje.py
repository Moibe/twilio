import bridges
from twilio.rest import Client

account_sid = bridges.account_sid
auth_token = bridges.au
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+5215534002530'
)

print(message.sid)