#!/usr/bin/env python
import pika
import json

credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = '172.17.0.2' , port=5672, credentials=credentials))

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='http://mess_rabbt'))
channel = connection.channel()
channel.queue_declare(queue='post_processing_2_gateway')
def callback(ch, method, properties, body):
    print( json.loads( body )[ "url" ] )
    print( "Received" )
    #connection.close( )

channel.basic_consume(
    queue='post_processing_2_gateway', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
