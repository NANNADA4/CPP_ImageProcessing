# app.py
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('entry.html')


@app.route('/main')
def info():
    return render_template('main.html')


@app.route("/server", methods=["POST"])
def server():
    option = request.form['ImageProcess']
    if (option == 'Histogram'):
        return histogram()
    elif (option == 'Equlization'):
        return equlization()
    elif (option == 'BasicContrast'):
        return basic()
    else:
        return endsin()


def histogram():
    return 'hello, histogram'


def equlization():
    return 'hello, equlization'


def basic():
    return 'hello, basic'


def endsin():
    return 'hello, endsin'


if __name__ == "__main__":
    app.run(debug=True)
