import random
from time import sleep
from uuid import uuid4

import requests

from flask import (
    Blueprint, request, jsonify,
    json,
    make_response,
    Response,
    stream_with_context,
    send_file
)

from sequencer import cache
from sequencer.default_settings import MOCK_BLAST_HAS_RESULTS, USE_GIS_CACHING, BLAST_TIMEOUT
from sequencer.support import ev3_reader
from sequencer.db import db
from sequencer.models import Sequence, TaxonNames
from sequencer.support.blaster import blast_sequence, blast_sequence_local
from sequencer.support.ev3_reader import query_full_sequence

GCE_KEY = None
GCE_PROJECT_CX = None
BLAST_DB_DIR = None


class APIBlueprint(Blueprint):
    def register(self, app, options, first_registration=False):
        global GCE_KEY, GCE_PROJECT_CX

        config = app.config
        GCE_KEY = config.get('GCE_KEY')
        GCE_PROJECT_CX = config.get('GCE_PROJECT_CX')
        BLAST_DB_DIR = config.get('BLAST_DB_DIR')

        super(APIBlueprint, self).register(app, options, first_registration)


bp = APIBlueprint('api', __name__, url_prefix='/api')

BASE_MAPPING = {
    'green':  'A',
    'blue':   'C',
    'red':    'T',
    'yellow': 'G'
}


@bp.route('/ping')
def ping():
    return jsonify({'msg': 'pong!'})


# ------------------------------------------------------
# --- LEGO Brick Comm.
# ------------------------------------------------------

@bp.route('/nudge/<direction>', defaults={'amount': 1})
@bp.route('/nudge/<direction>/<amount>')
def nudge(direction, amount):
    return jsonify(ev3_reader.nudge(direction, amount=float(amount)))


@bp.route('/query_ev3')
def query_ev3():
    username = request.args.get('username', 'anonymous')

    def save_to_db(uname, sequence):
        candidate = Sequence(username=uname, sequence=sequence)
        db.session.add(candidate)
        db.session.commit()
        return candidate.id

    def g():
        readings = []

        yield "["  # delimiters are for whoever's waiting for a full sequence
        not_first = False
        for row in query_full_sequence():
            # delimit with commas
            if not_first:
                yield ','
            not_first = True

            readings.append(row)
            yield json.dumps(row)

        if not_first:
            yield ','
        yield json.dumps({'query_id': save_to_db(username, json.dumps(readings))})
        yield "]"

    try:
        if request.args.get('streaming') == 'true':
            return Response(stream_with_context(g()))
        else:
            payload = list(query_full_sequence())
            payload.append({'query_id': save_to_db(username, json.dumps(payload))})

            return jsonify(payload)

    except Exception as ex:
        # raise ex
        print(str(ex))
        return make_response(jsonify({
            'error': str(ex)
        }), 500)


# ------------------------------------------------------
# --- BLAST proxy
# ------------------------------------------------------

@bp.route('/blast')
def blast():
    try:
        sequence = request.args['sequence']
    except KeyError:
        return jsonify({'error': 'must specify a sequence'})

    def g():
        gen = blast_sequence(sequence, timeout=BLAST_TIMEOUT)
        not_first = False
        yield "["
        for rec in gen:
            if not_first:
                yield ","
            not_first = True
            yield json.dumps(rec)
        yield "]"

    # incrementally yields json objects
    return Response(stream_with_context(g()))


@bp.route('/local_blast')
def local_blast():
    try:
        sequence = request.args['sequence']
    except KeyError:
        return jsonify({'error': 'must specify a sequence'})

    def g():
        gen = blast_sequence_local(sequence, blast_db_dir=BLAST_DB_DIR)
        not_first = False
        yield "["
        for rec in gen:
            if not_first:
                yield ","
            not_first = True
            yield json.dumps(rec)
        yield "]"

    # incrementally yields json objects
    return Response(stream_with_context(g()))


# ------------------------------------------------------
# --- GIS species images
# ------------------------------------------------------

@bp.route('/species_img')
def species_img():
    species_name = request.args.get('species')
    # species_name = "Homo sapiens"

    cache_key = 'SPECIES_IMG:%s' % species_name
    cached_val = cache.get(cache_key) if USE_GIS_CACHING else None

    if not cached_val:
        resp = requests.get('https://www.googleapis.com/customsearch/v1/siterestrict', params={
            "key": GCE_KEY,
            "cx": GCE_PROJECT_CX,
            "safe": "high",
            "fileType": "png|jpg|gif",
            "imgType": "photo",
            "searchType": "image",
            "limit": 1,
            "q": species_name
        })
        result = resp.json()

        try:
            cached_val = [x['link'] for x in result['items']]
            cache.set(cache_key, cached_val)
        except KeyError:
            # if we don't have any items, don't even bother udpating the cache and just return nothing
            cached_val = []

            return jsonify({'results': []})

        cache.set(cache_key, cached_val)

    return jsonify({
        'results': cached_val
    })


# ------------------------------------------------------
# --- taxonomic information
# ------------------------------------------------------

@bp.route('/taxonomy/<tax_id>')
def ancestry(tax_id):
    results = db.engine.execute("""
    with recursive ancestry(tax_id, rank, name) as (
        select taxons.tax_id, taxons.rank, taxon_names.name from taxons
        inner join taxon_names on taxon_names.tax_id=taxons.tax_id
        where taxons.tax_id=:tax_id
    
        union all
    
        select T.parent_tax_id, T.rank, TN.name
        from taxons T, ancestry
        inner join taxon_names TN on TN.tax_id=T.tax_id
        where T.tax_id=ancestry.tax_id and T.tax_id != T.parent_tax_id
    ) select * from ancestry;
    """, {'tax_id': tax_id})

    columns = [x.name for x in TaxonNames.__table__.columns]

    return jsonify({
        'ancestry': list(dict(zip(columns, x)) for x in results)
    })


# ------------------------------------------------------
# --- mocked endpoints
# ------------------------------------------------------

@bp.route('/mock_blast', methods=['GET','POST'])
def mock_blast():
    """
    Responds to our blaster module's requests in a feasible way
    :return:
    """

    arg_set = (request.form if request.method == 'POST' else request.args)
    command = arg_set.get('CMD')

    if command == 'Put':
        result_id = str(uuid4()).split('-')[0]
        estimated_time = random.randint(1, 5)

        return Response(
            ("    RID = %s" % result_id) + "\n" +
            ("    RTOE = %d" % estimated_time)
        )

    elif command == 'Get':
        if arg_set.get('FORMAT_OBJECT') == 'SearchInfo':
            # randomly decide on a status to return
            # (note that we've ommitted the failure status, 'UNKNOWN')
            # we could also return a non-parseable result like 'ASDADSA' to indicate no results
            # status = random.choice(('WAITING', 'READY'))
            status = 'READY'
            return Response(""""   Status=%s""" % status)

        elif arg_set.get('FORMAT_TYPE') == 'Text':
            # return something that looks like a result?
            return Response("""hello!""")

        elif arg_set.get('FORMAT_TYPE') == 'JSON2_S':
            return send_file("mockdata/canned_blast.json") if MOCK_BLAST_HAS_RESULTS else send_file("mockdata/canned_blast_noresults.json")

