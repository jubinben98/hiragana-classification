"""
Flask Backend
"""
import cv2 as cv
import numpy as np
import os
import pandas as pd
import tensorflow as tf
import time

from base64 import b64encode
from flask import Flask, flash, request, redirect, url_for, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = "Your_secret_string"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
class_map = np.array(pd.read_csv("assets/k49_classmap.csv")['char'])
model = tf.keras.models.load_model('hiragana_classifier_v1.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/submit", methods=['GET', 'POST'])
def process():

    if 'images' not in request.files:
        flash('No file part')
        return redirect(request.url)

    files = request.files.getlist('images')

    image_list = []
    file_str_list = []
    for file in files:
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # read image file string data
            filestr = file.read()
            # convert string data to numpy array
            file_bytes = np.frombuffer(filestr, np.uint8)
            # convert numpy array to image
            img = cv.imdecode(file_bytes, cv.IMREAD_UNCHANGED)
            if img.shape[-1] == 4:
                img = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
            else:
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            image_list.append(img)
            file_str_list.append(filestr)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

    predictions = model.predict(np.array(image_list)).argmax(axis=1)
    predictions = class_map[predictions]
    heading = ["Image", "Prediction"]

    images_uri = []
    for i in file_str_list:
        encoded = b64encode(i)
        decoded_img = encoded.decode('utf-8')
        mime = "image/png"
        uri = "data:%s;base64,%s" % (mime, decoded_img)
        images_uri.append(uri)

    return  render_template('result.html', table_heading=heading, images=images_uri, result=predictions)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8001)
