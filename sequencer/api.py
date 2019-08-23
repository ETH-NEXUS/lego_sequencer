from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify,
    json
)

from sequencer import ev3_reader
from sequencer.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


MOCK_COMM = False
BASE_MAPPING = {
    'green':  'A',
    'blue':   'C',
    'red':    'T',
    'yellow': 'G'
}


@bp.route('/ping')
def ping():
    return jsonify({'msg': 'pong!'})


@bp.route('/nudge/<direction>')
def nudge(direction):
    return jsonify(ev3_reader.nudge(direction))


@bp.route('/query_ev3')
def query_ev3():
    db = get_db()

    payload = ev3_reader.query_sequencer() if not MOCK_COMM else ev3_reader.query_sequencer_mock()

    # save it to the db before we proceed
    db.execute('insert into sequences (sequence) values (?)', (json.dumps(payload),))
    db.commit()

    return jsonify(payload)


@bp.route('/blast')
def blast():
    try:
        sequence = request.args['sequence']
    except KeyError:
        return jsonify({'error': 'must specify a sequence'})

    return jsonify({
        'response': sequence
    })
