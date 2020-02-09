#!/usr/bin/env python
import pika

#import libraries for radar visualization
# import numpy as np
# import datetime
# import pyart
# import boto
# import os
# import tempfile
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# #suppress deprecation warnings
# import warnings
import json
# warnings.simplefilter("ignore", category=DeprecationWarning)
from pytemperature import k2f
import urllib.request, json

appid_key = "e125e10d5beec79d36fd71a90cdc590c"


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='data_retrieval_2_model_execution')
channel.queue_declare(queue='model_execution_2_post_processing')

def sending( user_data ) :
    channel.basic_publish( exchange='', routing_key='model_execution_2_post_processing', body=user_data)
    print(" [x] Sent 'Hello World!'")
    connection.close()

def getData( user_url ) :
    with urllib.request.urlopen( user_url ) as url:
        data = json.loads(url.read().decode())
        return data

def current_weather( user_data ) :
    user_data_x = user_data[ "User" ]
    user_data_list = user_data_x.split( )
    #user_url = "http://api.openweathermap.org/data/2.5/weather?q=" + user_data_list[ 0 ] + "," + user_data_list[ 1 ] + "," + user_data_list[ 2 ] + "&appid=" + appid_key
    #user_url = "pro.openweathermap.org/data/2.5/forecast/hourly?q=" + user_data_list[ 0 ] + "," + user_data_list[ 1 ] + "," + user_data_list[ 2 ] + "&appid=" + appid_key
    user_url = "http://api.openweathermap.org/data/2.5/forecast?q=" + user_data_list[ 0 ] + "," + user_data_list[ 1 ] + "," + user_data_list[ 2 ] + "&appid=" + appid_key
    return getData( user_url )

def forecasting( user_data ) :
    forecast = [  ]
    body = user_data
    for i in range( 40 ) :
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
    return forecast

def callback(ch, method, properties, body):
    body = json.loads( body )
    user_data = current_weather( body )
    forecast_data = forecasting( user_data )
    all_data = { "Forecast" : forecast_data , "Processing" : body[ "Processing" ] , "User" : body[ "User" ] }
    sending( json.dumps( all_data ) )

channel.basic_consume(
    queue='data_retrieval_2_model_execution', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
