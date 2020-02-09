#!/usr/bin/env python
import pika
import json
from datetime import date

import numpy as np
import matplotlib.pyplot as plt
from numpy import ma

from metpy.cbook import get_test_data
from metpy.io.nexrad import Level2File
from metpy.plots import ctables

import boto3
import botocore
from botocore.client import Config

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='data_retrieval_2_model_execution')

channel.queue_declare(queue='gateway_2_data_retrieval')

def data_extraction( user_site , curr_date ) :
    s3 = boto3.resource('s3', config=Config(signature_version=botocore.UNSIGNED,
                                        user_agent_extra='Resource'))
    bucket = s3.Bucket('noaa-nexrad-level2')
    curr_date = str( curr_date ).split( '-' )
    if( len( curr_date[ 2 ] ) == 1 ) :
        curr_date[ 2 ] = "0" + curr_date[ 2 ]
    obj = ""
    for obj in bucket.objects.filter(Prefix= ( curr_date[ 0 ] + '/' + curr_date[ 1 ] + '/' + curr_date[ 2 ] + '/' + user_site + '/' \
                        + user_site + curr_date[ 0 ] + curr_date[ 1 ] + curr_date[ 2 ] + '_' ) ):#'2017/01/01/KTLX/KTLX20170101_'):
        #name = get_test_data('KTLX20130520_201643_V06.gz', as_file_obj=False)
        continue
    f = Level2File(obj.get()[ 'Body' ])
        #name = get_test_data(str( obj.key )[ 16: ] + '.gz' , as_file_obj=False)
        #f = Level2File(name)
    sweep = 0
    # First item in ray is header, which has azimuth angle
    az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])
    # #
    # # # 5th item is a dict mapping a var name (byte string) to a tuple
    # # # of (header, data array)
    ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
    ref_range = np.arange(ref_hdr.num_gates) * ref_hdr.gate_width + ref_hdr.first_gate
    ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])
    # #
    rho_hdr = f.sweeps[sweep][0][4][b'RHO'][0]
    rho_range = (np.arange(rho_hdr.num_gates + 1) - 0.5) * rho_hdr.gate_width + rho_hdr.first_gate
    rho = np.array([ray[4][b'RHO'][1] for ray in f.sweeps[sweep]])
    #
    plot_details = { "site" : user_site , "date" : curr_date , "ref_range" : ref_range.tolist() , "ref" : ref.tolist() , "rho_range" : rho_range.tolist() , "rho" : rho.tolist() , "az" : az.tolist() }
    # plot_details = { "site" : user_site , "date" : curr_date , "sweeps" : f.sweeps }
    return plot_details

def sending( user_data ) :
    user_data = json.loads( user_data )
    plot_details = data_extraction( user_data.split( )[ 3 ] , str( date.today( ) ) )
    #print( plot_details )
    forecast_processing = { "Processing" : plot_details , "User" : user_data }
    channel.basic_publish(exchange='', routing_key='data_retrieval_2_model_execution', body = json.dumps( forecast_processing ) )
    #print(" [x] Sent 'Hello World!'")
    connection.close()

def callback(ch, method, properties, body):
    sending( body )
    print(" [x] Received %r" % body)

channel.basic_consume(
    queue='gateway_2_data_retrieval', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
