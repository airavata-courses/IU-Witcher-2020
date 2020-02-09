#!/usr/bin/env python
import pika
import json
from pytemperature import k2f

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='post_processing_2_gateway')

def callback(ch, method, properties, body):
    print( json.loads( body )[ "url" ] )
    connection.close( )

channel.basic_consume(
    queue='post_processing_2_gateway', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
