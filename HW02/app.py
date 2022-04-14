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
    pixels = []

    for x in range(256):
        pixels.append(x)

    histoArray = np.zeros(256, dtype=int)

    for h in range(0, height):
        for w in range(0, width):
            Pixel = image.getpixel((w, h))
            histoArray[Pixel] += 1

    plt.bar(pixels, histoArray)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('showImg.html', plot_url=plot_url)


def equalization():
    image = Image.open('./static/SavedImages/lena_original.bmp')

    width = image.width
    height = image.height
    sum = 0
    scale_factor = 255 / height * width
    pixels = []
    comulativeArray = []
    sum_hist = []

    for x in range(256):
        pixels.append(x)
        comulativeArray.append(x)
        sum_hist.append(x)

    histoArray = np.zeros(256, dtype=int)

    for h in range(0, height):
        for w in range(0, width):
            Pixel = image.getpixel((w, h))
            histoArray[Pixel] += 1

    for y in range(256):
        sum += histoArray[y]
        sum_hist[y] = int(sum * scale_factor + 0.5)

    plt.bar(pixels, sum_hist)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    plot_url1 = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('showImg1.html', plot_url1=plot_url1)


def basic():
    image = Image.open('./static/SavedImages/lena_original.bmp')

    width = image.width
    height = image.height
    pixels = []
    min = 255
    max = 0

    for h in range(height):
        for w in range(width):
            Pixel = image.getpixel((w, h))
            if (Pixel < min):
                min = Pixel

    for h in range(height):
        for w in range(width):
            Pixel = image.getpixel((w, h))
            if (Pixel > max):
                max = Pixel

    for x in range(256):
        pixels.append(x)

    histoArray = np.zeros(256, dtype=int)

    for h in range(height):
        for w in range(width):
            Pixel = image.getpixel((w, h))
            newPixel = int(((Pixel - min) / (max - min)) * 255)
            histoArray[newPixel] += 1

    plt.bar(pixels, histoArray)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    plot_url2 = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('showImg2.html', plot_url2=plot_url2)


def endsin():
    image = Image.open('./static/SavedImages/lena_original.bmp')

    width = image.width
    height = image.height
    pixels = []
    min = 50
    max = 190

    for x in range(256):
        pixels.append(x)

    histoArray = np.zeros(256, dtype=int)

    for h in range(height):
        for w in range(width):
            Pixel = image.getpixel((w, h))

            if (Pixel < min):
                newPixel = 0
            elif(Pixel >= max):
                newPixel = 255
            else:
                newPixel = int(((Pixel - min) / (max - min)) * 255)

            histoArray[newPixel] += 1

    plt.bar(pixels, histoArray)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    plot_url2 = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('showImg2.html', plot_url2=plot_url2)


if __name__ == "__main__":
    app.run(debug=True)
