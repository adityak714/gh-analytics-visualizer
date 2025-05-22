import pulsar
import json
from get_number_of_commits import count_commits
import time

# Connect to Pulsar broker on VM4
client = pulsar.Client("pulsar://192.168.2.29:6650")

# Subscribe to the same topic the producer writes to
consumer = client.subscribe(
    'persistent://public/default/repos-raw',
    subscription_name='repo-subscription-for-commits', 
    consumer_type=pulsar.ConsumerType.Exclusive  # Allows multiple consumers to share load
)


print("\n\nListening for messages on topic: repos-raw\n\n")

list_of_repos=[]


try:
    while True:
        try:
            msg = consumer.receive(timeout_millis=1000)
            if msg.data() == b"__SHUTDOWN__":
                print("Received shutdown signal. Exiting.")
                consumer.acknowledge(msg)
                try:
                    t0 = time.time()
                    count_commits(list_of_repos)
                    t1 = time.time()
                    total = t1-t0
                    print(f"Total time it took: {total}s")
                except Exception as e:
                    print("Failed during analysis:", e)
                break  
            repo = json.loads(msg.data())
            list_of_repos.extend(repo)
            consumer.acknowledge(msg)
            print(f"Current amount of repos: {len(list_of_repos)}\n")
        except pulsar.Timeout:
            continue  # No message received in time, loop again
        except Exception as e:
            print("Failed to process message:", e)
            # Only negatively acknowledge if msg was defined
            if 'msg' in locals():
                consumer.negative_acknowledge(msg)


finally:
    consumer.close()
    client.close()

