import flask
import time
import unicornhat as unicorn

app = flask.Flask(__name__)
app.config["DEBUG"] = True

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()

def setColor(r,g,b):
    unicorn.clear()
    unicorn.set_all(r,g,b)
    unicorn.show()


@app.route('/red', methods=['GET'])
def red():
  setColor(255,45,0)
  return 'Red'

@app.route('/yellow', methods=['GET'])
def yellow():
  setColor(255,253,0)
  return 'Yellow'

@app.route('/green', methods=['GET'])
def green():
  setColor(0,224,55)
  unicorn.show()
  return 'Green'

@app.route('/off', methods=['GET'])
def off():
  unicorn.off()
  return 'Off'


app.run(host='0.0.0.0',port='5000')
