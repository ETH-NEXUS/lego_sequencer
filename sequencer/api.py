from flask import (
    Blueprint, request, jsonify,
    json,
    make_response,
    Response,
    stream_with_context
)

from sequencer.support import ev3_reader
from sequencer.db import get_db
from sequencer.support.ev3_reader import query_full_sequence

bp = Blueprint('api', __name__, url_prefix='/api')


MOCK_COMM = True
BASE_MAPPING = {
    'green':  'A',
    'blue':   'C',
    'red':    'T',
    'yellow': 'G'
}


@bp.route('/ping')
def ping():
    return jsonify({'msg': 'pong!'})


@bp.route('/nudge/<direction>', defaults={'amount': 1})
@bp.route('/nudge/<direction>/<amount>')
def nudge(direction, amount):
    return jsonify(ev3_reader.nudge(direction, amount=float(amount)))


@bp.route('/query_ev3')
def query_ev3():

    def g():
        db = get_db()
        readings = []

        yield "["  # delimiters are for whoever's waiting for a full sequence
        not_first = False
        for row in query_full_sequence(mock=MOCK_COMM):
            # delimit with commas
            if not_first:
                yield ','
            not_first = True

            readings.append(row)
            yield json.dumps(row)

        yield "]"

        db.execute('insert into sequences (sequence) values (?)', (json.dumps(readings),))
        db.commit()

    try:
        if request.args.get('streaming') == 'true':
            return Response(stream_with_context(g()))
        else:
            o_db = get_db()
            payload = list(query_full_sequence(mock=MOCK_COMM))
            o_db.execute('insert into sequences (sequence) values (?)', (json.dumps(payload),))
            o_db.commit()

            return jsonify(payload)

    except Exception as ex:
        # raise ex
        print(str(ex))
        return make_response(jsonify({
            'error': str(ex)
        }), 500)


@bp.route('/blast')
def blast():
    try:
        sequence = request.args['sequence']
    except KeyError:
        return jsonify({'error': 'must specify a sequence'})

    # TODO: send the sequence, then wait for a response

    return jsonify({
        'response': sequence
    })
