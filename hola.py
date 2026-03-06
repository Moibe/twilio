from twilio.rest import Client
import bridges

account_sid = bridges.account_sid
auth_token = bridges.au
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
  content_variables='{"1":"12/1","2":"3pm"}',
  to='whatsapp:+5215534002530'
)

print(message)
print(message.price)
print(vars(message))
