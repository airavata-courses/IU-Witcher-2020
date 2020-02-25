#!/usr/bin/env python
# importing necessary libraries
import pika
import json
from datetime import date

import numpy as np
# import matplotlib.pyplot as plt
# from numpy import ma

# from metpy.cbook import get_test_data
from metpy.io.nexrad import Level2File
# from metpy.plots import ctables

import boto3
import botocore
from botocore.client import Config

# establishing connection to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declaring receiving queue
channel.queue_declare(queue='data_retrieval_2_model_execution')
# declaring sending queue
channel.queue_declare(queue='gateway_2_data_retrieval')

def data_extraction( user_site , curr_date ) :
    s3 = boto3.resource(
        's3',
         config = Config(
            signature_version = botocore.UNSIGNED,
            user_agent_extra = 'Resource'
        )
    )
    bucket = s3.Bucket('noaa-nexrad-level2')
    # making list of dates [ yyyy , mm , dd ]
    curr_date = str( curr_date ).split( '-' )
    # making the date of correct format( yyyy/mm/dd )
    if( len( curr_date[ 2 ] ) == 1 ) :
        curr_date[ 2 ] = "0" + curr_date[ 2 ]
    # iterating through all the elements in the list
    # temporary variable
    temp2 = ''
    for obj in bucket.objects.filter(Prefix= ( curr_date[ 0 ] + '/' + curr_date[ 1 ] + '/' + curr_date[ 2 ] + '/' + user_site + '/' \
                        + user_site + curr_date[ 0 ] + curr_date[ 1 ] + curr_date[ 2 ] + '_' ) ):#'2017/01/01/KTLX/KTLX20170101_'):
        #f = Level2File(obj.get()[ 'Body' ])
        # temporary variable for location
        temp1 = temp2
        # to access the second most recent time
        temp2 = obj
    # after finding the latest element in the NEXRAD AWS directory
    # as per the current time.
    # Downloading that file
    f = Level2File(temp1.get()[ 'Body' ])
    # extracting mathemtical data from the weather data's class
    # to be passed upon in the future.
    sweep = 0
    # First item in ray is header, which has azimuth angle
    az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])
    # 5th item is a dict mapping a var name (byte string) to a tuple
    # of (header, data array)
    ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
    ref_range = np.arange(ref_hdr.num_gates) * ref_hdr.gate_width + ref_hdr.first_gate
    ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])
    rho_hdr = f.sweeps[sweep][0][4][b'RHO'][0]
    rho_range = (np.arange(rho_hdr.num_gates + 1) - 0.5) * rho_hdr.gate_width + rho_hdr.first_gate
    rho = np.array([ray[4][b'RHO'][1] for ray in f.sweeps[sweep]])
    # converting all numpy arrays to list to be passed on as JSON objects
    plot_details = { "site" : user_site , "date" : curr_date , "ref_range" : ref_range.tolist() , "ref" : ref.tolist() , "rho_range" : rho_range.tolist() , "rho" : rho.tolist() , "az" : az.tolist() }
    return plot_details

def sending( user_data ) :
    # converting json data to dictionary
    user_data = json.loads( user_data )
    # using user site and current date for accessing its weather directory
    plot_details = data_extraction( user_data.split( )[ 3 ] , str( date.today( ) ) )
    # Making a dictionary of the elements to be used
    forecast_processing = { "Processing" : plot_details , "User" : user_data }
    # sending the merged data
    channel.basic_publish(exchange='', routing_key='data_retrieval_2_model_execution', body = json.dumps( forecast_processing ) )
    connection.close()

def callback(ch, method, properties, body):
    # calling the sending process
    sending( body )
    print(" [x] Received %r" % body)

# consuming process
channel.basic_consume(
    queue='gateway_2_data_retrieval', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
# start consuming process
channel.start_consuming()
