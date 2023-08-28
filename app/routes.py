import cv2 as cv
import numpy as np
import os
import pandas as pd
import tensorflow as tf
from flask import flash, request, redirect, url_for, render_template
from base64 import b64encode
from app import app
from app.utils import allowed_file, FilesConfig

MODEL = tf.keras.models.load_model(FilesConfig.model_name)
CLASS_MAP = np.array(pd.read_csv(FilesConfig.class_map)['char'])

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for("landing_page"))

@app.route("/landing_page")
def landing_page():
    """Render the index page."""
    return render_template('index.html')

@app.route("/submit", methods=['GET', 'POST'])
def process():
    """
    Process uploaded images, perform predictions, and render the result page.

    This route handles image uploads, reads and processes them, performs predictions,
    and renders the result page with images and their corresponding predictions.
    """
    if 'images' not in request.files:
        message = 'No file part found'
        flash(message)
        return redirect(url_for("landing_page"))

    files = request.files.getlist('images')

    image_list = []
    file_str_list = []
    for file in files:
        if file.filename == '':
            message = 'No image selected for uploading'
            flash(message)
            return redirect(url_for("landing_page"))

        if file and allowed_file(file.filename):
            # read image file string data
            file_str = file.read()
            # convert string data to numpy array
            file_bytes = np.frombuffer(file_str, np.uint8)
            # convert numpy array to image
            img = cv.imdecode(file_bytes, cv.IMREAD_UNCHANGED)
            if img.shape[-1] == 4:
                img = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
            else:
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            image_list.append(img)
            file_str_list.append(file_str)
        else:
            message = 'Allowed image types are - png, jpg, jpeg, gif'
            flash(message)
            return redirect(url_for("landing_page"))

    predictions = MODEL.predict(np.array(image_list)).argmax(axis=1)
    predictions = CLASS_MAP[predictions]
    heading = ["Image", "Prediction"]

    images_uri = []
    for i in file_str_list:
        encoded = b64encode(i)
        decoded_img = encoded.decode('utf-8')
        mime = "image/png"
        uri = "data:%s;base64,%s" % (mime, decoded_img)
        images_uri.append(uri)

    return render_template('result.html', table_heading=heading, images=images_uri, result=predictions)
