from flask import Flask,redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
# cors = CORS(app)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

import urllib
import json
import pika
import requests

temp=''

@app.route('/',methods=['GET'])
def indexPage():
    uname=request.args.get('username')
    password=request.args.get('password')

    if uname=='guest':
        return "Successfully logged in"

    print("got user credentials")
    params = urllib.parse.urlencode({'username': uname, 'password': password})
    content = urllib.request.urlopen(
        'http://user-management?%s' % params).read().decode('utf-8')
    print('response from php: ',content)
    if "True" in content:
        print("userId after logged in")
        return "Successfully logged in"
    else:
        return "Wrong Password"

@app.route('/signup',methods=['POST','GET'])
def signupPage():
    uname=request.args.get('username')
    password=request.args.get('password')
    print("signing up user")
    params = urllib.parse.urlencode({'username': uname, 'password': password}).encode("utf-8")
    content = urllib.request.urlopen(
        'http://user-management/',params).read().decode('utf-8')
    print('response from php: ', content)
    if "Successfully" in content:
        return "Successfully Created User"
    else:
        return "User Already Exists"

@app.route('/data',methods=['POST','GET','PUT','OPTIONS'])
def data():
    if request.method == 'POST':
        user_data=json.dumps(request.form['search'])
        return "weather put"

    elif request.method == 'PUT':
        user_data = json.dumps(request.form)
        print('user data', user_data)
        return "weather put"

    else:
        userID=request.args.get('username')
        search=request.args.get('search')

        print( "Search " , request.args.get('search'))

        credentials = pika.PlainCredentials(username='guest', password='guest')
        try:
        	connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host = 'message-broker' , port=5672, credentials=credentials))
        except:
        	print("Error occured while making connection")
        	return "Error occured while making connection to rabbitMQ"

        channel = connection.channel()
        channel.queue_declare(queue='gateway_2_data_retrieval')
        user_data=json.dumps(request.args.get('search'))
        #user_data = json.dumps("Bloomington Indiana USA KIND")



        def callback(ch, method, properties, body):
            #sending(body)
            global temp
            temp=json.loads(body)
            print( "Forecast" , temp[ "Forecast" ][ 0 ] )
            #return str(temp[ "Forecast" ][ 0 ])
            #return str(temp[ "Forecast" ][ 0 ])
            connection.close()

            #print(" [x] Received %r" % body)
        print( "About to publish" )
        channel.basic_publish(exchange='', routing_key='gateway_2_data_retrieval', body=user_data)
        channel.queue_declare(queue='post_processing_2_gateway')
        print( "Publish" )
        channel.basic_consume(
            queue='post_processing_2_gateway', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        return str(temp[ "Forecast" ][ 0 ])

        # check if user entry exists in mongodb

        url = "http://149.165.171.53:32171/"

        dict={'userName':userID,'search':search,'prediction':temp[ "Forecast" ][ 0 ]}
        try:
            response = requests.get('http://149.165.171.53:32171/'+userID)
            print( "Content" , response.content)
            res_dict = json.loads(response.content.decode('utf-8'))

            if 'userName' in res_dict:
                r=requests.put(url,json=dict)
                print("put request",r.content)
                #r = json.loads(r.content.decode('utf-8'))
            else:
                r = requests.post(url,json=dict)
                print("post request",r.content)
                #r = json.loads(r.content.decode('utf-8'))
        except:
            return  str(temp[ "Forecast" ][ 0 ])

        return str(temp[ "Forecast" ][ 0 ])


@app.route('/history',methods=['POST','GET','PUT'])
def gethistory():
    if request.method == 'GET':
        userID=request.args.get('username')
        url = "http://149.165.171.53:32171/"
        try:
            response = requests.get('http://149.165.171.53:32171/')
            print("Get response" ,response.content)
            res_dict = json.loads(response.content.decode('utf-8'))
        except:
            return "Error while getting session information"

        return str(res_dict)

if __name__ == '__main__':
    app.run(debug= True,host='0.0.0.0')
