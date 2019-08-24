#!/usr/bin/env python

import os
from flask import Flask, render_template, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename

from sequencer.support import ev3_reader
from debugging.parsing import parse_raw

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return None

    file = request.files['file']

    if file.filename == '':
        return None

    if file and allowed_file(file.filename):
        print("Got file, saving...")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return filepath

    return None


@app.route('/query_ev3')
def query_ev3():
    return jsonify(ev3_reader.query_sequencer())


@app.route('/debug', methods=['GET', 'POST'])
def debug():
    if request.method == 'POST':
        filepath = handle_upload()

        if filepath:
            rows = parse_raw(filepath)
            return render_template('debug.html', **{
                'contents': rows
            })
        else:
            flash('No selected file')
            return redirect(request.url)

    return render_template('debug.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')
