#!/usr/bin/env python

from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder="./frotend/dist", template_folder="./frontend/dist")

from sequencer.support import ev3_reader


@app.route('/query_ev3')
def query_ev3():
    return jsonify(ev3_reader.query_sequencer())


@app.route('/')
def index():
    return render_template("index.html")
