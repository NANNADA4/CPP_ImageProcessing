import base64
from datetime import datetime
from functools import update_wrapper, wraps
from io import BytesIO
import math
import matplotlib.pyplot as plt
from PIL import Image
from flask import Flask, make_response, render_template, request, flash
import numpy as np
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = "--"


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
    return render(request.form['option'])


def render(option):
    raw_show = open_raw(option)
    dct_show = make_dct(option)
    if (option == 'ex01'):
        return render_template('ex01.html', raw_show=raw_show, dct_show=dct_show)
    else:
        return render_template('ex02.html', raw_show=raw_show, dct_show=dct_show)


def open_file(option):
    if (option == 'ex01'):
        return open("./static/resource/lena_raw_512x512.raw")
    else:
        return open("./static/resource/BOAT512.raw")


def open_raw(option):
    fid = open_file(option)
    img = np.fromfile(fid, dtype='uint8', sep='')
    fid.close()
    img = np.reshape(img, [512, 512])

    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)
    raw_show = base64.b64encode(img.getvalue()).decode('utf8')

    return raw_show


def make_dct(option):
    fid = open_file(option)

    # B_size = 8

    # for i in range(0, 40):
    #     zz = math.pi * float(i+1) / 64.0
    #     c[i] = math.cos(zz)
    #     s[i] = math.sin(zz)


if __name__ == "__main__":
    app.run(debug=True)
