#!/bin/sh

export FLASK_APP=sequencer
export FLASK_ENV=development
pipenv run python waitress_server.py
