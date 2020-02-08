#!/usr/bin/env python
import pika
import json
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='gateway_2_data_retrieval')

#user_data = json.dumps( { "City" : "Bloomington" , "State" : "Indiana" , "Country" : "USA" } )

user_data = json.dumps( "Bloomington Indiana USA KIND" )

#user_data =  { "City" : "Bloomington" , "State" : "Indiana" , "Country" : "USA" }

channel.basic_publish( exchange = '' , routing_key = 'gateway_2_data_retrieval' , body = user_data )
print(" [x] Sent 'Hello World!'")
connection.close()
