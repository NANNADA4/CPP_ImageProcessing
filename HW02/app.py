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

        img = Image.open(file_path).convert("L")

        # 이미지 리사이징
        img = np.resize(img, (1, 784))

        test_data = ((np.array(img) / 255) - 1) * -1

        # 모델 불러오기
        model = load_model("./Predict_Model.h5")

        # 클래스 예측 함수에 가공된 테스트 데이터 넣어 결과 도출
        predict_x = model.predict(test_data)
        res = np.argmax(predict_x, axis=1)

        return str(res)


if __name__ == "__main__":
    app.run(debug=True)
