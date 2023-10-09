from google.cloud import pubsub_v1

service_account_key_path = 'C:\\Users\\mchan\\Downloads\\key.json'
topic_name = 'projects/pricebook-etl-stage/topics/pricebook-test'

publisher = pubsub_v1.PublisherClient.from_service_account_file(service_account_key_path)

def publish_message(topic_path, message):
    future = publisher.publish(topic_path, message.encode('utf-8'))
    print(f"Published message: {message}")
    future.result()

# Publish some example messages
messages_to_publish = ["Message 1", "Message 2", "Message 3"]

for message in messages_to_publish:
    publish_message(topic_name, message)
