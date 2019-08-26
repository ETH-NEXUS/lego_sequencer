#!/usr/bin/env python

from waitress import serve
from sequencer import create_app
serve(create_app(), host='0.0.0.0', port=5000, threads=16)
