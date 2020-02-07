#!/usr/bin/env python
import pika
import json
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='data_retrieval_2_model_execution')

channel.queue_declare(queue='messenger_2_data_retrieval')

def sending( user_data ) :
    channel.basic_publish(exchange='', routing_key='data_retrieval_2_model_execution', body=user_data)
    print(" [x] Sent 'Hello World!'")
    connection.close()

def callback(ch, method, properties, body):
    sending( body )
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue='messenger_2_data_retrieval', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
