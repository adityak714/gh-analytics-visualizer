import pulsar
import json
from test_driven_development_analysis import analyze_tdd_and_ci_languages
import time
import os

token = os.getenv("GITHUB_TOKEN")

# Connect to Pulsar broker on VM4
client = pulsar.Client("pulsar://192.168.2.29:6650")

# Subscribe to the same topic the producer writes to
consumer = client.subscribe(
    'persistent://public/default/repos-raw',
    subscription_name='repo-subscription-for-test-and-ci',  # Unique subscription name
    consumer_type=pulsar.ConsumerType.Exclusive  # Allows multiple consumers to share load
)

print("\n\nListening for messages on topic: repos-raw\n\n")

#Create an empty list for the repos
list_of_repos=[]


try:
    while True:
        try:
            msg = consumer.receive(timeout_millis=1000)
            # If we recieve the msg "__SHUTDOWN__", we know that there are no more messages in 
            # persistent://public/default/repos-raw, hence we can start processing the data we've recieved
            if msg.data() == b"__SHUTDOWN__":
                print("Received shutdown signal. Exiting.")
                # Acknowledge the message
                consumer.acknowledge(msg)
                try:
                    #Start timer to check how long it takes to process list_of_repos and answer Q2
                    t0 = time.time()
                    # Call function analyze_tdd_and_ci_languages that obtains the most 
                    # frequent languages for repositories with testing and continuous integration 
                    # respectively 
                    analyze_tdd_and_ci_languages(list_of_repos, token)
                    
                    t1 = time.time()
                    total = t1-t0
                    
                    print(f"Total time it took: {total}s")
                except Exception as e:
                    print("Failed during analysis:", e)
                break  
            # If not recieved "__SHUTDOWN__", extend list_of_repos with the data that has been recieved from pulsar
            repo = json.loads(msg.data())
            list_of_repos.extend(repo)
            # Acknowledge the message
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

