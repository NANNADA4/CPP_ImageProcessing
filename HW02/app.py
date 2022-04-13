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


@app.route("/server", methods=["GET", "POST"])
def server():
    if request.method == "POST":
        file_name = request.files["file"]
        file_name.save("./static/images/" +
                       secure_filename(file_name.filename))
        file_path = "./static/images/" + str(file_name.filename)

        img = Image.open(file_path)


if __name__ == "__main__":
    app.run(debug=True)
