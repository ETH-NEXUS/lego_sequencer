from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)

bp = Blueprint(
    'frontend', __name__, url_prefix='/',
    static_folder="../frontend/dist", template_folder="../frontend/dist"
)


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')               # url /books will fail into here
def index(path):
    if path:
        return bp.send_static_file(path)
    return bp.send_static_file('index.html')


# @bp.route('/static/<path:path>')
# def static_file(path):
#     return bp.send_static_file(path)
