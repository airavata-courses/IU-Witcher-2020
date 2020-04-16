#!/usr/bin/env python
# importing necessary libraries
import pika
import json
from datetime import date

import numpy as np
from numpy import ma

from metpy.io.nexrad import Level2File

import boto3
import botocore
from botocore.client import Config

# establishing connection to RabbitMQ server
credentials = pika.PlainCredentials( username = 'guest' , password = 'guest' )
connection = pika.BlockingConnection( pika.ConnectionParameters(
            host = 'message-broker' , port = 5672 , credentials = credentials ) )
channel = connection.channel( )

# declaring receiving queue
channel.queue_declare( queue = 'data_retrieval_2_model_execution' )

def data_extraction( user_site ) :
    s3 = boto3.resource(
        's3' ,
         config = Config(
            signature_version = botocore.UNSIGNED ,
            user_agent_extra = 'Resource'
        )
    )
    bucket = s3.Bucket('noaa-nexrad-level2')
    # making list of dates [ yyyy , mm , dd ]
    curr_date = str( date.today( ) ).split( '-' )
    # making the date of correct format( yyyy/mm/dd )
    if( len( curr_date[ 2 ] ) == 1 ) :
        curr_date[ 2 ] = "0" + curr_date[ 2 ]
    # iterating through all the elements in the list
    # temporary variable
    last = ''
    for obj in bucket.objects.filter( Prefix = ( curr_date[ 0 ] + '/' + curr_date[ 1 ] + '/' + curr_date[ 2 ] + '/' + user_site + '/' \
                        + user_site + curr_date[ 0 ] + curr_date[ 1 ] + curr_date[ 2 ] + '_' ) ):
        # temporary variable for location
        second_last = last
        # to access the second most recent time
        last = obj
    # after finding the latest complete element in the NEXRAD AWS directory
    # as per the current time.
    # Downloading that file
    f = Level2File( second_last.get( )[ 'Body' ] )
    # extracting mathemtical data from the weather data's class
    # to be passed upon in the future.
    sweep = 0
    # First item in ray is header, which has azimuth angle
    az = np.array( [ ray[ 0 ].az_angle for ray in f.sweeps[ sweep ] ] )
    # 5th item is a dict mapping a var name (byte string) to a tuple
    # of (header, data array)
    ref_hdr = f.sweeps[ sweep ][ 0 ][ 4 ][ b'REF' ][ 0 ]
    ref_range = np.arange( ref_hdr.num_gates ) * ref_hdr.gate_width + ref_hdr.first_gate
    ref = np.array( [ ray[ 4 ][ b'REF' ][ 1 ] for ray in f.sweeps[ sweep ] ] )
    rho_hdr = f.sweeps[ sweep ][ 0 ][ 4 ][ b'RHO' ][ 0 ]
    rho_range = ( np.arange( rho_hdr.num_gates + 1 ) - 0.5 ) * rho_hdr.gate_width + rho_hdr.first_gate
    rho = np.array( [ ray[ 4 ][ b'RHO' ][ 1 ] for ray in f.sweeps[ sweep ] ] )
    # converting all numpy arrays to list to be passed on as JSON objects
    plot_details = { "site" : user_site , "date" : curr_date , "ref_range" : ref_range.tolist() , "ref" : ref.tolist() , "rho_range" : rho_range.tolist() , "rho" : rho.tolist() , "az" : az.tolist() }
    return plot_details

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
