import pulsar
import json

#Function that sends list of repositories to pulsar
def send_to_pulsar(repo, shutdown):
    #Create a pulsar client that connects to the broker on VM1
    client = pulsar.Client("pulsar://192.168.2.29:6650")
        #Create a producer that publishes the messages on the topic "repos-raw"
    producer = client.create_producer("persistent://public/default/repos-raw")
    
    # Check if we want to shutdown
    if shutdown == False:
        # If shutdown = false, we send the repos as producer
        # Loops throug every reposotiry in the list
        producer.send(json.dumps(repo).encode('utf-8'))

    # If we want to shutdown, we send "__SHUTDOWN__" which will shutdown the system
    else:
        producer.send(b"__SHUTDOWN__")
    #Close producer and close connection to client when all messages has been sent
    producer.close()
    client.close()
