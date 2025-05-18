import pulsar
import os
import json


def send_to_pulsar(repo):
    client = pulsar.Client("pulsar://130.238.28.110:6650")
    producer = client.create_producer("persistent://public/default/repos-raw")

    for repos in repo:
        producer.send(json.dumps(repos).encode('utf-8'))

    producer.close()
    client.close()
