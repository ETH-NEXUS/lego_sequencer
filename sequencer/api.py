from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)

from sequencer import ev3_reader
from sequencer.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/ping')
def ping():
    return jsonify({'msg': 'pong!'})


@bp.route('/query_ev3')
def query_ev3():
    db = get_db()
    payload = jsonify(ev3_reader.query_sequencer())

    # save it to the db before we proceed
    db.execute('insert into sequences (sequence) values (?)', (payload.data,))
    db.commit()

    return payload
