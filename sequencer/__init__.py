from flask import json
import os

from flask import Flask
from flask_cors import CORS

from sequencer.cache import cache

# set up logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('sequencer.default_settings')
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'sequencer.sqlite'),
        BLAST_DB_DIR=os.path.join(app.root_path, 'blast_db'),
        # CACHE_DIR=os.path.join(app.instance_path, 'cache'),
        # CACHE_TYPE="filesystem",
        SQLALCHEMY_DATABASE_URI="sqlite:///%s" % os.path.join(app.instance_path, 'sequencer.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    app.config.from_pyfile('application.cfg', silent=False)

    #print('config: {}'.format(app.config))
    # allow the dev server to hit our api, too
    CORS(app, resources={r'/*': {'origins': '*'}})
    # also enable caching backend
    cache.init_app(app, config={
        'CACHE_DIR': os.path.join(app.instance_path, 'cache'),
        'CACHE_TYPE': "filesystem"
    })

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # inject database management
    from . import db
    db.db.init_app(app)
    app.cli.add_command(db.init_db_command)

    # inject api endpoints
    from . import api
    app.register_blueprint(
        api.bp,
        GCE_KEY=app.config['GCE_KEY'],
        GCE_PROJECT_CX=app.config['GCE_PROJECT_CX'],
        BLAST_DB_DIR=app.config['BLAST_DB_DIR']
    )

    # inject frontend-serving bits
    from . import frontend
    app.register_blueprint(frontend.bp)

    return app
