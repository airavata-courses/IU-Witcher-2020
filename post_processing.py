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

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='model_execution_2_post_processing')

channel.queue_declare(queue='post_processing_2_gateway')

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

    plt.savefig( "Reflectivity.png" )
    #plt.show()

def sending( user_data ) :
    plotting( json.loads( user_data )[ "Processing" ] )
    channel.basic_publish(exchange='', routing_key='post_processing_2_gateway', body=user_data)
    print(" [x] Sent 'Hello World!'")
    connection.close()

def callback(ch, method, properties, body):
    sending( body )
    #print(" [x] Received %r" % body)


channel.basic_consume(
    queue='model_execution_2_post_processing', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
