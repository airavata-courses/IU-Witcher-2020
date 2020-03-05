#!/usr/bin/env python
import pika
import json
import time

time.sleep( 10 )

credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = 'rabbit' , port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='gateway_2_data_retrieval')

user_data = json.dumps( "Bloomington Indiana USA KIND" )

channel.basic_publish( exchange = '' , routing_key = 'gateway_2_data_retrieval' , body = user_data )
print(" [x] Sent 'Hello World!'")
#connection.close()
channel.basic_publish( exchange = '' , routing_key = 'gateway_2_data_retrieval' , body = user_data )
print(" [x] Sent 'Hello World!'")
