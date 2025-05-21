import pulsar
import json
from test_driven_development_analysis import analyze_tdd_and_ci_languages

# Connect to Pulsar broker on VM4
client = pulsar.Client('pulsar://130.238.29.220:6650')

# Subscribe to the same topic the producer writes to
consumer = client.subscribe(
    'persistent://public/default/repos-raw',
    subscription_name='repo-subscription',  # Unique subscription name
    consumer_type=pulsar.ConsumerType.Shared  # Allows multiple consumers to share load
)

print("Listening for messages on topic: repos-raw")


try:
    while True:
        # Wait for a message
        msg = consumer.receive()
        print(type(msg))
        # 
        try:
            # Decode JSON message
            repo = json.loads(msg.data())
            # Acknowledge successful processing
            consumer.acknowledge(msg)
        except Exception as e:
            print("Failed to process message:", e)
            consumer.negative_acknowledge(msg)    
except KeyboardInterrupt:
    print("\nStopping consumer.")

# Clean up
consumer.close()
client.close()


