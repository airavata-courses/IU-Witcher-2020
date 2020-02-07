#!/usr/bin/env python
import pika
import json
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

x = json.dumps( { 'site' : "KDOX" , "date" :
"12/01/2020" } )

channel.basic_publish(exchange='', routing_key='hello', body=x)
print(" [x] Sent 'Hello World!'")
connection.close()
