import flask
import time
import unicornhat as unicorn

app = flask.Flask(__name__)
app.config["DEBUG"] = True

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()


@app.route('/red', methods=['GET'])
def red():
  unicorn.clear()
  unicorn.set_all(255,45,0)
  unicorn.show()
  return 'Red'

@app.route('/yellow', methods=['GET'])
def yellow():
  unicorn.clear()
  unicorn.set_all(255,253,0)
  unicorn.show()
  return 'Yellow'

@app.route('/green', methods=['GET'])
def green():
  unicorn.clear()
  unicorn.set_all(0,224,55)
  unicorn.show()
  return 'Green'

@app.route('/off', methods=['GET'])
def off():
  unicorn.off()
  return 'Off'


app.run(host='0.0.0.0',port='5000')
