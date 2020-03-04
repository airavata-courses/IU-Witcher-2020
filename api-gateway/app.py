from flask import Flask,redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import urllib
import json
import pika
import requests


userID=''

@app.route('/',methods=['GET'])
def indexPage():
    uname=request.args.get('uname')
    password=request.args.get('password')
    content = urllib.request.urlopen(
        'http://phpserver?uname=' + uname + '&password=' + password).read().decode('utf-8')
    print('response from php: ',content)
    if "True" in content:
        global userID
        userID = uname
        print("userId after logged in",userID)
        return "Successfully logged in"
    else:
        return "Wrong Password"

@app.route('/signup',methods=['POST','GET'])
def signupPage():
    if request.method == 'POST':
        uname=request.form['uname']
        password=request.form['password']
        content = urllib.request.urlopen('http://localhost/WeatherAppSignUp.php?uname='+uname+'&password='+password).read().decode('utf-8')
        print('response from php: ', content)
        if content=="User Created Successfully":
            return "Successfully Created User"
        else:
            return "User Already Exists"

    else:
        uname=request.args.get('uname')
        password=request.args.get('password')
        #return "logged in"
        #return "get method %S "% user
        content = urllib.request.urlopen(
            'http://localhost/WeatherAppSignUp.php?uname=' + uname + '&password=' + password).read().decode('utf-8')
        print('response from php: ', content)
        if content == "User Created Successfully":
            return "Successfully Created User"
        else:
            return "User Already Exists"

@app.route('/data',methods=['GET'])
def data():
        search=request.args.get('search')
        print(request.args.get('search'))
        credentials = pika.PlainCredentials(username='guest', password='guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq-server', port=5672, credentials=credentials))
        #connection = pika.BlockingConnection(pika.ConnectionParameters('http://rabbitMq'))
        print(connection)
        channel = connection.channel()
        channel.queue_declare(queue='gateway_2_data_retrieval')
        channel.queue_declare(queue='post_processing_2_gateway')

        user_data=json.dumps(request.args.get('search'))
        #user_data = json.dumps("Bloomington Indiana USA KIND")

        def callback(ch, method, properties, body):
            #sending(body)
            global temp
            temp = body
            temp=json.loads(temp)
            print( temp[ "Forecast" ][ 0 ] )
            connection.close()

            #print(" [x] Received %r" % body)

        channel.basic_publish(exchange='', routing_key='gateway_2_data_retrieval', body=user_data)

        channel.basic_consume(
            queue='post_processing_2_gateway', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


        # check if user entry exists in mongodb

        #url = "http://localhost:4321/users"
        return str(temp["Forecast"][0])


@app.route('/history',methods=['POST','GET','PUT'])
def gethistory():
    if request.method == 'GET':
        url = "http://localhost:4321/users"
        global userID
        response = requests.get('http://localhost:4321/users/'+userID)
        print(response.content)
        res_dict = json.loads(response.content.decode('utf-8'))

        return str(res_dict)



if __name__ == '__main__':
    app.run(debug= True,host='0.0.0.0' )
