from google.cloud import pubsub_v1

service_account_key_path = 'C:\\Users\\mchan\\Downloads\\key.json'
subscription_name = 'pricebook-test-sub'

subscriber = pubsub_v1.SubscriberClient.from_service_account_file(service_account_key_path)

def callback(message):
    message_data = message.data.decode('utf-8')
    print(f"Received message: {message_data}")
    message.ack()
    print("Msg Received Succesfully")


subscription_path = subscriber.subscription_path('pricebook-etl-stage', subscription_name)
subscriber.subscribe(subscription_path, callback=callback)

print(f"Listening for messages on {subscription_path}")
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Interrupted, message receiving stops")