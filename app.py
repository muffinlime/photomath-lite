import os
import datetime
from flask import Flask, render_template, request
import cv2
import main

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files['file']
        path = os.path.join("./uploads", file.filename)
        file.save(path)
        dt = str(datetime.datetime.now())
        os.rename(path, os.path.join("./uploads", "image_"+dt+".jpg"))
        image = cv2.imread(os.path.join("./uploads", "image_"+dt+".jpg"))
        (expression, result) = main.full(image)
        str_expression = ' '.join(map(str, expression))
        return render_template('result.html', expression=str_expression, result=result)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)