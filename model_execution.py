#!/usr/bin/env python
# importing necessary libraries
import pika
import json
from pytemperature import k2f
import urllib.request, json

appid_key = "e125e10d5beec79d36fd71a90cdc590c"

import time
# time to start rabbitmq server
time.sleep( 10 )

# establishing connection to RabbitMQ server
credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = 'message-broker' , port=5672, credentials=credentials))
channel = connection.channel()

# declaring receiving queue
channel.queue_declare(queue='data_retrieval_2_model_execution')
# declaring sending queue
channel.queue_declare(queue='model_execution_2_post_processing')


# getting data from url
def getData( user_url ) :
    with urllib.request.urlopen( user_url ) as url:
        # load the website to dictionary
        data = json.loads(url.read().decode())
        return data

def current_weather( user_data ) :
    # using user city , state , country , site
    user_data_x = user_data[ "User" ]
    user_data_list = user_data_x.split( )
    #user_url = "http://api.openweathermap.org/data/2.5/weather?q=" + user_data_list[ 0 ] + "," + user_data_list[ 1 ] + "," + user_data_list[ 2 ] + "&appid=" + appid_key
    #user_url = "pro.openweathermap.org/data/2.5/forecast/hourly?q=" + user_data_list[ 0 ] + "," + user_data_list[ 1 ] + "," + user_data_list[ 2 ] + "&appid=" + appid_key
    # for forecasting weather
    user_url = "http://api.openweathermap.org/data/2.5/forecast?q=" + user_data_list[ 0 ] + "," + user_data_list[ 1 ] + "," + user_data_list[ 2 ] + "&appid=" + appid_key
    return getData( user_url )

def forecasting( user_data ) :
    forecast = [  ]
    body = user_data
    # filtering the forecast data got from the api call
    # 40 here implies every 3 hours data for 5 days so
    # 24 / 3 x 5
    for i in range( 40 ) :
        # make a temporary dictionary
        # which stores all the important values as dictionary elements
        temp = { }
        curr_dir = body[ "list" ][ i ]
        temp[ "temp" ] = k2f( curr_dir[ "main" ][ "temp" ] )
        temp[ "temp_min" ] = k2f( curr_dir[ "main" ][ "temp_min" ] )
        temp[ "temp_max" ] = k2f( curr_dir[ "main" ][ "temp_max" ] )
        temp[ "humidity" ] = curr_dir[ "main" ][ "humidity" ]
        temp[ "weather" ] = curr_dir[ "weather" ][ 0 ][ "main" ]
        temp[ "wind_speed" ] = curr_dir[ "wind" ][ "speed" ]
        temp[ "date_time" ] = curr_dir[ "dt_txt" ]
        forecast.append( temp )
    # returning complete list of forecast which has all elements as dictionary
    return forecast

def sending( user_data ) :
    # sending the merged data
    channel.basic_publish( exchange='', routing_key='model_execution_2_post_processing', body=user_data)
    print(" [x] Sent 'Hello World!'")
    connection.close()

def callback(ch, method, properties, body):
    # making it dictionary
    body = json.loads( body )
    user_data = current_weather( body )
    forecast_data = forecasting( user_data )
    # making dictionary with all elements from prevous and current to one dictionary
    all_data = { "Forecast" : forecast_data , "Processing" : body[ "Processing" ] , "User" : body[ "User" ] }
    # calling the sending process
    sending( json.dumps( all_data ) )

# print( "Model exec" )
# channel.basic_consume(
#     queue='data_retrieval_2_model_execution', on_message_callback=callback, auto_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
while True :
    channel.basic_consume(
        queue='data_retrieval_2_model_execution', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    print( "Model Executed" )
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                host = 'message-broker' , port=5672, credentials=credentials))
    channel = connection.channel()
#
#     # declaring receiving queue
#     channel.queue_declare(queue='data_retrieval_2_model_execution')
#     # declaring sending queue
#     channel.queue_declare(queue='model_execution_2_post_processing')
