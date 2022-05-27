import base64
from cmath import sqrt
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


img = Image.open("./static/SavedImages/lena_bmp_512x512_new.bmp").convert('L')
img = np.array(img)

roberts_1 = np.array([[1, 0],
                      [0, -1]])

roberts_2 = np.array([[0, -1],
                      [1, 0]])

sobel_x = np.array([[-1/4, 0, 1/4],
                    [-2/4, 0, 2/4],
                    [-1/4, 0, 1/4]])

sobel_y = np.array([[1/4, 2/4, 1/4],
                    [0, 0, 0],
                    [-1/4, -2/4, -1/4]])

prewitt_x = np.array([[-1/3, 0, 1/3],
                      [-1/3, 0, 1/3],
                      [-1/3, 0, 1/3]])

prewitt_y = np.array([[1/3, 1/3, 1/3],
                      [0, 0, 0],
                      [-1/3, -1/3, -1/3]])

stochastic_x = np.array([[0.267, 0.364, 0, -0.364, -0.267],
                         [0.373, 0.562, 0, -0.562, -0.373],
                         [0.463, 1.000, 0, -1.000, -0.463],
                         [0.373, 0.562, 0, -0.562, -0.373],
                         [0.267, 0.364, 0, -0.364, -0.267]])

stochastic_y = stochastic_x.T


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
        flash("올바른 옵션을 선택해주세요")
        return render_template('ex01.html')
    elif(option == 'Roberts'):
        flash("Roberts Edge Detection을 선택하셨습니다.")
        return edge_detection(img, roberts_1, roberts_2, threshold=150)
    elif(option == 'Sobel'):
        flash("Sobel Edge Detection을 선택하셨습니다.")
        return edge_detection(img, sobel_x, sobel_y, threshold=150)
    elif(option == 'Prewitt'):
        flash("Prewitt Edge Detection을 선택하셨습니다.")
        return edge_detection(img, prewitt_x, prewitt_y, threshold=150)
    elif(option == 'Stochastic'):
        flash("Stochastic Edge Detection을 선택하셨습니다.")
        return edge_detection(img, stochastic_x, stochastic_y, threshold=150)


def edge_detection(img, mask1, mask2, threshold):

    img_shape = img.shape

    try:
        if mask1.shape != mask2.shape:
            raise Exception('마스크의 크기가 서로 다릅니다.')
        filter_size = mask1.shape
    except Exception as e:
        print('예외가 발생했습니다.', e)

    result_shape = tuple(np.array(img_shape)-np.array(filter_size)+1)

    result1 = np.zeros(result_shape)
    result2 = np.zeros(result_shape)

    for h in range(0, result_shape[0]):
        for w in range(0, result_shape[1]):
            tmp = img[h:h+filter_size[0], w:w+filter_size[1]]
            result1[h, w] = np.abs(np.sum(tmp*mask1))
            result2[h, w] = np.abs(np.sum(tmp*mask2))

    result = result1 + result2

    thr_result = np.zeros(result_shape)
    thr_result[result > threshold] = 1

    plt.imshow(thr_result, cmap='gray')
    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)
    img_show = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('ex01.html', img_show=img_show)


if __name__ == "__main__":
    app.run(debug=True)
