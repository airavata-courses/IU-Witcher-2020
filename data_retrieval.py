#!/usr/bin/env python
# importing necessary libraries
import pika
import json
from datetime import date

# establishing connection to RabbitMQ server
credentials = pika.PlainCredentials( username = 'guest' , password = 'guest' )
connection = pika.BlockingConnection( pika.ConnectionParameters(
            host = 'message-broker' , port = 5672 , credentials = credentials ) )
channel = connection.channel( )

# declaring receiving queue
channel.queue_declare( queue = 'data_retrieval_2_model_execution' )

def sending( radar_input_data ) :
    # converting json data to dictionary
    radar_input_data = json.loads( radar_input_data )
    # using user site and current date for accessing its weather directory
    plot_details = ""#data_extraction( radar_input_data.split( )[ -1 ].upper( ) )
    # Making a dictionary of the elements to be used
    forecast_processing = { "Processing" : plot_details , "User" : radar_input_data }
    # sending the merged data
    channel.basic_publish( exchange = '' , routing_key = 'data_retrieval_2_model_execution' , body = json.dumps( forecast_processing ) )
    connection.close( )

def callback( ch , method , properties , body ) :
    # calling the sending process
    sending( body )

while True :
    channel.basic_consume(
        queue = 'gateway_2_data_retrieval' , on_message_callback = callback , auto_ack = True )
    channel.start_consuming( )
    print( "Data retrieved" )
    connection = pika.BlockingConnection( pika.ConnectionParameters(
                host = 'message-broker' , port = 5672 , credentials = credentials ) )
    channel = connection.channel( )
