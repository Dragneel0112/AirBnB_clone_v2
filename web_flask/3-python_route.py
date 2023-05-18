#!/usr/bin/python3
'''
Starts Flask web application
'''
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    '''Displays str Hello HBNB!'''
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    ''' Displays HBNB on path /hbnb'''
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    ''' Displays C as well as text on path '''
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    '''Displays python is cool as default or text on path '''
    text = text.replace('_', ' ')
    return "Python  {}".format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
