from flask import Flask, request
import numpy as np
import cv2
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return "Server has started successfully.\n"

"""
@app.route("/instant_ngp", methods=['POST'])
def process():
    files = request.files
    images = dict()
    for f in ['source', 'target']:
        _bytes = np.frombuffer(files[f].read(), np.uint8)
        images[f] = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
    remapped = estimate_opticalflow(images['source'], images['target'])
    _, dst_data = cv2.imencode('.jpg', remapped)
    dst_base64 = base64.b64encode(dst_data).decode('utf-8')

    return dst_base64
"""