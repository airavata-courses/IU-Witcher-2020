#!/usr/bin/env python
import pika
import json
from pytemperature import k2f

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='post_processing_2_gateway')

def callback(ch, method, properties, body):
    forecast = [  ]
    body = json.loads( body )
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
    print( forecast )

    #print(" [x] Received %r" % body)

channel.basic_consume(
    queue='post_processing_2_gateway', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
