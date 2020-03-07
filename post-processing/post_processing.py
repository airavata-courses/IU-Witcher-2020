#!/usr/bin/env python
# importing necessary libraries
import sys
import pika
import json

import numpy as np
import matplotlib.pyplot as plt
from numpy import ma

from metpy.plots import ctables , add_timestamp
from datetime import datetime

import boto
import boto3
import boto.s3
from boto.s3.key import Key
from botocore.client import Config

import time

# time to start rabbitmq server
time.sleep( 5 )


# establishing connection to RabbitMQ server
credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = 'rabbit' , port=5672, credentials=credentials))
channel = connection.channel()

# declaring receiving queue
channel.queue_declare(queue='model_execution_2_post_processing')
# declaring sending queue
channel.queue_declare(queue='post_processing_2_gateway')

# hosting the image files
def hosting( ) :
    # Uncomment this
    #AWS_ACCESS_KEY_ID = Your AWS Acess Key ID
    #AWS_SECRET_ACCESS_KEY = Your AWS SECRET KEY

    AWS_ACCESS_KEY_ID = 'AKIAJ22HE5TX46NA33GA'
    AWS_SECRET_ACCESS_KEY = 'Ccjf6xc5GcJl89fCN1LyEtqbZl0mMOu7OuoW7ay4'

    # using predefined bucket in AWS
    bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)

    # connecting bucket to be used
    bucket = conn.create_bucket(bucket_name,
        location=boto.s3.connection.Location.DEFAULT)

    testfile = "Reflectivity_Correlation.png"
    print( 'Uploading %s to Amazon S3 bucket %s' % \
       (testfile, bucket_name) )

    # showcasing the uploading of file
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    k = Key(bucket)
    k.key = 'mytestfile'
    k.set_contents_from_filename(testfile,
        cb=percent_cb, num_cb=10)
    s3 = boto3.client('s3')
    # making the file public
    k.set_acl('public-read')
    # predesignated url
    return "https://akiaiphw3bwx2yojao4a-dump.s3.amazonaws.com/mytestfile"
    #return url

# plotting Reflectivity range
def plotting( plot_data ) :
    # acessing dictionary data and making it into numpy
    # arrays so that it can be used for doing mathemtical operations
    # and plotting values
    ref_range = np.array( plot_data[ "ref_range" ] )
    rho_range = np.array( plot_data[ "rho_range" ] )
    ref = np.array( plot_data[ "ref" ] )
    rho = np.array( plot_data[ "rho" ] )
    az = np.array( plot_data[ "az" ] )
    fig, axes = plt.subplots(1, 2, figsize=(15, 8))
    for var_data, var_range, ax in zip( ( ref , rho ) , ( ref_range , rho_range ) , axes ) :
        # Turn into an array, then mask
        data = ma.array(var_data)
        data[np.isnan(data)] = ma.masked
        # Convert az,range to x,y
        xlocs = var_range * np.sin(np.deg2rad(az[:, np.newaxis]))
        ylocs = var_range * np.cos(np.deg2rad(az[:, np.newaxis]))
        # Plot the data
        cmap = ctables.registry.get_colortable('viridis')
        ax.pcolormesh(xlocs, ylocs, data, cmap=cmap)
        ax.set_aspect('equal', 'datalim')
        ax.set_xlim(-40, 20)
        ax.set_ylim(-30, 30)
        add_timestamp(ax, datetime.now(), y=0.02, high_contrast=True)
    # Labelling plot
    fig.suptitle( 'Minimum and Maximum range of Reflectivity' )
    # saving the file to be used in future
    plt.savefig( "Reflectivity_Correlation.png" )
    #return "https://akiaiphw3bwx2yojao4a-dump.s3.amazonaws.com/mytestfile"
    return hosting( )

def sending( user_data ) :
    x = plotting( json.loads( user_data )[ "Processing" ] )
    user_data = json.loads( user_data )
    user_data[ "url" ] = x
    # sending the merged data
    print( "About to send" )
    channel.basic_publish(exchange='', routing_key='post_processing_2_gateway', body=json.dumps( user_data ))
    print(" [x] Sent 'Hello World!'")
    connection.close()

def callback(ch, method, properties, body):
    # calling the sending process
    sending( body )

# print( "Post proc" )
# # consming process
# channel.basic_consume(
#     queue='model_execution_2_post_processing', on_message_callback=callback, auto_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# # start consuming process
# channel.start_consuming()
while True :
    channel.basic_consume(
        queue='model_execution_2_post_processing', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    print( "Post processed" )
    #time.sleep( 5 )
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                host = 'rabbit' , port=5672, credentials=credentials))
    channel = connection.channel()
#
#     # declaring receiving queue
#     channel.queue_declare(queue='model_execution_2_post_processing')
#     # declaring sending queue
#     channel.queue_declare(queue='post_processing_2_gateway')
