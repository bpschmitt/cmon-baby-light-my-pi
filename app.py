import flask
import time
import unicornhat as unicorn

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/red', methods=['GET'])
@app.route('/yellow', methods=['GET'])
@app.route('/green', methods=['GET'])

def red():
    return "<h1>Red</h1>"

def yellow():
    return "<h1>Yellow</h1>"

def green():
    return "<h1>Green</h1>"

app.run(host='0.0.0.0',port='5000')
