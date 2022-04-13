import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO, StringIO
import matplotlib.pyplot as plt
from PIL import Image
from flask import Flask, Response, render_template, request, send_file
import numpy as np
import matplotlib
matplotlib.use('Agg')

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
            histoArray[Pixel] = histoArray[Pixel] + 1

    plt.plot(histoArray)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    # return send_file(img, mimetype='image/png')
    return render_template('showImg.html', plot_url=plot_url)


def equalization():
    return 'hello, equlization'


def basic():
    return 'hello, basic'


def endsin():
    return 'hello, endsin'


if __name__ == "__main__":
    app.run(debug=True)
