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

# import time
# time to start rabbitmq server
# time.sleep( 10 )

import pyimgur
CLIENT_ID = "34e5e22dcc85836"
image_link = pyimgur.Imgur(CLIENT_ID)


# establishing connection to RabbitMQ server
credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = 'message-broker' , port=5672, credentials=credentials))
channel = connection.channel()

# declaring receiving queue
channel.queue_declare(queue='model_execution_2_post_processing')
# declaring sending queue
channel.queue_declare(queue='post_processing_2_gateway')

# hosting the image files

def image_hosting( ) :
    uploaded_image = image_link.upload_image('Reflectivity_Correlation.png', title="Image Hosted")
    # print( uploaded_image.link )
    return str( uploaded_image.link )

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
    return image_hosting( )

def sending( user_data ) :
    x = plotting( json.loads( user_data )[ "Processing" ] )
    user_data = json.loads( user_data )
    user_data[ "url" ] = x
    # sending the merged data
    channel.basic_publish(exchange='', routing_key='post_processing_2_gateway', body=json.dumps( user_data ) )
    connection.close()

def callback(ch, method, properties, body):
    # calling the sending process
    sending( body )

while True :
    channel.basic_consume(
        queue='model_execution_2_post_processing', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    print( "Post processed" )
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                host = 'message-broker' , port=5672, credentials=credentials))
    channel = connection.channel()
