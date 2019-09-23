import click
from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from sequencer.default_settings import LOAD_TAXON_DATA

db = SQLAlchemy()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    import sequencer.models
    db.init_app(current_app)
    db.create_all()
    click.echo('Initialized the database.')

    if LOAD_TAXON_DATA:
        sequencer.models.load_taxons(click.echo)
        click.echo('Loaded taxons from dump.')
