from twilio.rest import Client

account_sid = "AC17ad69a6fcb1089cd9e216678de7604a"
auth_token = "cd3130f61186847163ed46c3cccfef47"

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="VehicleCheck",
                     from_='+12813368905',
                     to='+919725569102'
                 )
print(message.sid)