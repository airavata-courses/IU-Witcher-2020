from flask import Flask,redirect, url_for, request, jsonify
import urllib
import json

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def indexPage():
    if request.method == 'POST':
        uname=request.form['uname']
        password=request.form['password']
        content = urllib.request.urlopen('http://localhost/WeatherAppLogin.php?uname='+uname+'&password='+password).read().decode('utf-8')
        print('response from php: ', content)
        if content=="True":
            return "Successfully logged in"
        else:
            return "Wrong Password"

    else:

        uname=request.args.get('uname')
        password=request.args.get('password')
        #return "logged in"
        #return "get method %S "% user
        content = urllib.request.urlopen(
            'http://localhost/WeatherAppLogin.php?uname=' + uname + '&password=' + password).read().decode('utf-8')
        print('response from php: ', content)
        if content == "True":
            return "Successfully logged in"
        else:
            return "Wrong Password"


@app.route('/<name>')
def hello_world(name):
    return 'Hello World! %s' % name




if __name__ == '__main__':
    app.run(debug= True )
