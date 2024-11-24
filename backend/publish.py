from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = "projects/class-activity-435807/topics/my-topic"

try:
    future = publisher.publish(topic_path, b'Test message')
    print(f"Published message with ID: {future.result()}")
except Exception as e:
    print(f"Error publishing message: {e}")
