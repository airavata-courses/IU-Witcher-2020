#!/usr/bin/env python
# importing necessary libraries
import sys
import pika
import json

# establishing connection to RabbitMQ server
credentials = pika.PlainCredentials( username = 'guest' , password = 'guest' )
connection = pika.BlockingConnection( pika.ConnectionParameters(
            host = 'message-broker' , port = 5672 , credentials = credentials ) )
channel = connection.channel()

def callback(ch, method, properties, body):
    user_data = json.loads( body )
    image_url = ""#plotting( user_data[ "Processing" ] )
    processed_data = { "Forecast" : user_data[ "Forecast" ] , "url" : image_url }
    channel.basic_publish( exchange = '' , routing_key = 'post_processing_2_gateway' , body = json.dumps( processed_data ) )
    connection.close()

while True :
    channel.basic_consume(
        queue='model_execution_2_post_processing', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    print( "Post processed" )
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                host = 'message-broker' , port=5672, credentials=credentials))
    channel = connection.channel()
