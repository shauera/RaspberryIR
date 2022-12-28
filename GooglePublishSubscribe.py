# must set GOOGLE_APPLICATION_CREDENTIALS env var to the file containing the private key to authenticate against google cloud

import os
import json
from google.cloud import pubsub_v1
from google.oauth2.service_account import Credentials
from irrp import main

# print(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'missing!!!'))

# TODO(developer)
project_id = "homecontrol-dde07"
topic_id = "ControlCommands"

# the file content is deposited in github as a repository secret
# publisher_key_file = 'homecontrol_dde07_publisher_private_key_on_rapsberry_pi'
# api_key_publisher_credentials = Credentials.from_service_account_file(publisher_key_file)
# publisher = pubsub_v1.PublisherClient(credentials = api_key_publisher_credentials)

# # The `topic_path` method creates a fully qualified identifier
# # in the form `projects/{project_id}/topics/{topic_id}`
# topic_path = publisher.topic_path(project_id, topic_id)

# for n in range(1, 10):
#     data_str = f"Message number {n}"
#     # Data must be a bytestring
#     data = data_str.encode("utf-8")
#     # When you publish a message, the client returns a future.
#     future = publisher.publish(topic_path, data)
#     print(future.result())

# print(f"Published messages to {topic_path}.")

#----------------------------------------------------------------------------------------
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

subscription_id = "ControlCommands-sub"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

# the file content is deposited in github as a repository secret
subscriber_key_file = 'homecontrol_dde07_subscriber_private_key_on_rapsberry_pi'
api_key_subscriber_credentials = Credentials.from_service_account_file(subscriber_key_file)
subscriber = pubsub_v1.SubscriberClient(credentials = api_key_subscriber_credentials)
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    message.ack()
    print("------Received------")
    print(vars(message))
    print("--------------------")
    main(is_record_mode=False, gpio_pin=17, file_name='light_remote_control.ircodes', code_ids=['livingRoomArea'])

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

