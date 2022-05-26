import base64
from datetime import datetime
from functools import update_wrapper, wraps
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
from flask import Flask, make_response, render_template, request, flash
import numpy as np
import matplotlib
matplotlib.use('Agg')


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


app = Flask(__name__)
app.secret_key = "--"


@app.route('/')
@nocache
def index():
    return render_template('entry.html')


@app.route('/main')
@nocache
def info():
    return render_template('main.html')


@app.route('/ex01')
@nocache
def ex01():
    return render_template('ex01.html')


@app.route('/ex02')
@nocache
def ex02():
    return render_template('ex02.html')


@app.route('/server', methods=["POST"])
@nocache
def server():
    option = request.form['edge']
    if(option == 'Default'):
        return default()
    elif(option == 'Roberts'):
        return roberts()
    elif(option == 'Sobel'):
        return sobel()
    elif(option == 'Prewitt'):
        return prewitt()
    elif(option == 'Stochastic'):
        return stochastic()


def default():
    flash("올바른 옵션을 선택해주세요")
    return render_template('ex01.html')


def AddGaussian():
    return


def roberts():
    img = Image.open("./static/SavedImages/lena_bmp_512x512_new.bmp")
    img = np.array(img)

    roberts_1 = np.array([[1, 0], [0, -1]])
    roberts_2 = np.array([[0, 1], [-1, 0]])

    img_shape = img.shape

    return 0


def sobel():
    return


def prewitt():
    return


def stochastic():
    return


if __name__ == "__main__":
    app.run(debug=True)
