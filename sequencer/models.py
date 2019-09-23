import datetime

from tqdm import tqdm

from sequencer.db import db


# --------------------------------------------------------------------------------
# --- sequence query logging
# --------------------------------------------------------------------------------

class Sequence(db.Model):
    """
    Saves searched sequences along with the user who saved it.

    TODO: In the future, we'll also save the BLAST results, but for now it's always null.
    """

    __tablename__ = 'sequences'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now())
    username = db.Column(db.Text)
    sequence = db.Column(db.Text, nullable=False)
    results = db.Column(db.Text)

    def __init__(self, username=None, sequence=None):
        self.username = username
        self.sequence = sequence

    def __repr__(self):
        return '<Sequence %s>' % self.sequence


# --------------------------------------------------------------------------------
# --- taxonomic info models
# --------------------------------------------------------------------------------

class Taxon(db.Model):
    """
    Table of taxonomic data, from ftp://ftp.ncbi.nih.gov/pub/taxonomy/ (specifically the nodes.dmp file). Note that this
    table includes all levels of the taxonomic tree; the organizational level is stored in the 'rank' field.

    TODO: In the future, we'll use this to allow ordering/filtering of organism results by their taxonomic relationships,
    e.g. prioritizing "fuzzy things", filtering out viruses/bacteria, etc.
    """
    __tablename__ = 'taxons'
    tax_id = db.Column(db.BigInteger, primary_key=True)  # node id in GenBank taxonomy database
    parent_tax_id = db.Column(db.BigInteger, db.ForeignKey('taxons.tax_id'))  # parent node id in GenBank taxonomy database
    rank = db.Column(db.Text)  # rank of this node (superkingdom, kingdom, ...)
    embl_code = db.Column(db.Text)  # locus-name prefix; not unique
    division_id = db.Column(db.Text)  # see division.dmp file
    inherited_div_flag = db.Column(db.Boolean)  # 1 if node inherits division from parent
    genetic_code_id = db.Column(db.Text)  # see gencode.dmp file
    inherited_GC__flag = db.Column(db.Boolean)  # 1 if node inherits genetic code from parent
    mitochondrial_genetic_code_id = db.Column(db.BigInteger)  # see gencode.dmp file
    inherited_MGC_flag = db.Column(db.Boolean)  # 1 if node inherits mitochondrial gencode from parent
    GenBank_hidden_flag = db.Column(db.Boolean)  # 1 if name is suppressed in GenBank entry lineage
    hidden_subtree_root_flag = db.Column(db.Boolean)  # 1 if this subtree has no sequence data yet
    comments = db.Column(db.Text)  # free-text comments and citations


class TaxonNames(db.Model):
    """
    Like the Taxon model, contains information about organisms based on a tax_id returned from NCBI's services.

    This table stores scientific and, in some cases, common names of organisms for a given tax_id.
    """
    __tablename__ = 'taxon_names'
    tax_id = db.Column(db.BigInteger, primary_key=True)  # the id of node associated with this name
    name = db.Column(db.Text)  # name itself
    unique_name = db.Column(db.Text)  # the unique variant of this name if name not unique
    name_class = db.Column(db.Text)  # (synonym, common name, ...)


# ---
# --- helper routines for loading taxon data
# ---

def _load_table(table_obj, source_file, columns, filter_expr=None, transform_expr=None, recs_before_commit=5000):
    """
    Loads a columnar file's rows as a series of table_obj instances.
    :param table_obj: the model instance to load
    :param source_file: the name of the column-based file
    :param columns: the columns to load from the file into the model (field names and column names must match)
    :param filter_expr: a function applied to each row that, if returns falsey, will exclude that row
    :param transform_expr: a function applied to each row that can transform values in each cell of the row
    :param recs_before_commit: number of records to process before issuing a commit
    :return: None
    """

    # first, clear out any existing contents
    db.session.query(table_obj).delete()

    with open(source_file) as fp:
        commit_counter = recs_before_commit
        for row in tqdm(fp.readlines()):
            cells = dict(zip(columns, (x.strip() for x in row.split("|"))))

            # discards rows that don't pass the filter expression
            if filter_expr is not None and not filter_expr(cells):
                continue

            # transforms column values for this row in-place
            if transform_expr is not None:
                transform_expr(cells)

            db.session.add(table_obj(**cells))

            if commit_counter > 0:
                commit_counter -= 1
            else:
                commit_counter = recs_before_commit
                db.session.commit()

        db.session.commit()


def load_taxons(echoer):
    echoer("Loading taxon names...")
    _load_table(TaxonNames, './data/names.dmp', [
        'tax_id',
        'name',
        'unique_name',
        'name_class'
    ], filter_expr=lambda x: x['name_class'] == 'scientific name')

    def transform_bools(cells):
        for k in cells:
            if k.endswith('_flag'):
                cells[k] = bool(int(cells[k]))
        return cells

    echoer("Loading taxons...")
    _load_table(Taxon, './data/nodes.dmp', [
        'tax_id',
        'parent_tax_id',
        'rank',
        'embl_code',
        'division_id',
        'inherited_div_flag',
        'genetic_code_id',
        'inherited_GC__flag',
        'mitochondrial_genetic_code_id',
        'inherited_MGC_flag',
        'GenBank_hidden_flag',
        'hidden_subtree_root_flag',
        'comments',
    ], transform_expr=transform_bools)
