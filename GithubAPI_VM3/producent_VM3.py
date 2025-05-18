import pulsar
import json

#Function that sends list of repositories to pulsar
def send_to_pulsar(repo):
    #Create a pulsar client that connects to the broker on VM1
    client = pulsar.Client("pulsar://130.238.28.110:6650")
    #Create a producer that publishes the messages on the topic "repos-raw"
    producer = client.create_producer("persistent://public/default/repos-raw")

    # Loops throug every reposotiry in the list
    for repos in repo:
        #Convert to Json string
        producer.send(json.dumps(repos).encode('utf-8'))

    #Close producer and close connection to client when all messages has been sent
    producer.close()
    client.close()
