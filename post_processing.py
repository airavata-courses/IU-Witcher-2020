#!/usr/bin/env python
import pika
import json
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='model_execution_2_post_processing')

channel.queue_declare(queue='post_processing_2_gateway')

def sending( user_data ) :
    channel.basic_publish(exchange='', routing_key='post_processing_2_gateway', body=user_data)
    print(" [x] Sent 'Hello World!'")
    connection.close()

def callback(ch, method, properties, body):
    sending( body )
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue='model_execution_2_post_processing', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
