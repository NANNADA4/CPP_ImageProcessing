import base64
from datetime import datetime
from functools import update_wrapper, wraps
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
from flask import Flask, make_response, render_template, request
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


@app.route('/')
@nocache
def index():
    return render_template('entry.html')


@app.route('/main')
@nocache
def info():
    return render_template('main.html')


@app.route("/server", methods=["POST"])
@nocache
def server():
    option = request.form['ImageProcess']
    if (option == 'Histogram'):
        return histogram()
    elif (option == 'Equlization'):
        return equalization()
    elif (option == 'BasicContrast'):
        return basic()
    else:
        return endsin()


def histogram():
    image = Image.open('./static/SavedImages/lena_original.bmp')

    width = image.width
    height = image.height

    histoArray = np.zeros(255, dtype=int)

    for h in range(0, height):
        for w in range(0, width):
            Pixel = image.getpixel((w, h))
            histoArray[Pixel] += 1

    plt.plot(histoArray)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('showImg.html', plot_url=plot_url)


def equalization():
    image = Image.open('./static/SavedImages/lena_original.bmp')

    width = image.width
    height = image.height

    histoArray = np.zeros(255, dtype=int)
    comulativeArray = np.zeros(255, dtype=int)

    for h in range(0, height):
        for w in range(0, width):
            Pixel = image.getpixel((w, h))
            histoArray[Pixel] += 1

    comulativeArray = np.multiply(histoArray, 255 / (512 * 512)).astype('int')

    plt.plot(comulativeArray)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    plot_url1 = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('showImg1.html', plot_url1=plot_url1)


def basic():
    return 'hello, basic'


def endsin():
    return 'hello, endsin'


if __name__ == "__main__":
    app.run(debug=True)
