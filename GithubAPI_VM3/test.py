import pulsar

client = pulsar.Client("pulsar://192.168.2.29:6650")
producer = client.create_producer("persistent://public/default/repos-raw")
producer.send(b'{"hello": "world"}')
producer.close()
client.close()