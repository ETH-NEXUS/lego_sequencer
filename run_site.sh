#!/usr/bin/env bash

export FLASK_APP=sequencer
pipenv run python waitress_server.py
