#!/usr/bin/env python
import pika
import json

import numpy as np
import matplotlib.pyplot as plt
from numpy import ma

import json

from metpy.cbook import get_test_data
from metpy.io.nexrad import Level2File
from metpy.plots import ctables

import boto3
import botocore
from botocore.client import Config

import boto
import boto.s3
import sys
from boto.s3.key import Key

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='model_execution_2_post_processing')

channel.queue_declare(queue='post_processing_2_gateway')

def hosting( ) :
    # Uncomment this
    #AWS_ACCESS_KEY_ID = Your AWS Acess Key ID
    #AWS_SECRET_ACCESS_KEY = Your AWS SECRET KEY

    bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)

    bucket = conn.create_bucket(bucket_name,
        location=boto.s3.connection.Location.DEFAULT)

    testfile = "GINI_Water_Vapor.png"
    print( 'Uploading %s to Amazon S3 bucket %s' % \
       (testfile, bucket_name) )

    def percent_cb(complete, total):

        sys.stdout.write('.')
        sys.stdout.flush()

    k = Key(bucket)
    #k.set_acl('public-read')
    k.key = 'mytestfile'
    k.set_contents_from_filename(testfile,
        cb=percent_cb, num_cb=10)
    s3 = boto3.client('s3')
    k.set_acl('public-read')

    url = "https://akiaiphw3bwx2yojao4a-dump.s3.amazonaws.com/mytestfile"
    return url

def plotting( plot_data ) :

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

    plt.savefig( "GINI_Water_Vapor.png" )
    return hosting( )
    #plt.show()

def sending( user_data ) :
    x = plotting( json.loads( user_data )[ "Processing" ] )
    user_data = json.loads( user_data )
    user_data[ "url" ] = x
    channel.basic_publish(exchange='', routing_key='post_processing_2_gateway', body=json.dumps( user_data ))
    print(" [x] Sent 'Hello World!'")
    connection.close()

def callback(ch, method, properties, body):
    sending( body )
    #print(" [x] Received %r" % body)


channel.basic_consume(
    queue='model_execution_2_post_processing', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
