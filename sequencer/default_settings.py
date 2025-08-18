# -----------------------------------
# --- LEGO Sequencer Mocking
# -----------------------------------

# if true, mocks communication with the LEGO brick, producing sequences from real organisms
# (see support.ev3_reader.SAMPLE_SEQUENCES for details)
MOCK_COMM =  False

# if MOCK_COMM=True, the mock process duration is multiplied by this value (>1.0 slower, <1.0 faster)
TIME_MOD = 0.1

# if MOCK_COMM=True and if USE_RANDOM_SEQ=True, uses a random sequence of {A,C,T,G} instead of a sample sequence
USE_RANDOM_SEQ = False


# -----------------------------------
# --- NCBI BLAST:
# -----------------------------------

# time in seconds before the BLAST request times out, never if None
BLAST_TIMEOUT = 120

# minimum time in seconds between re-checking polls, since BLAST will occasionally return tiny values like 2 seconds
# set to 0 to disable the minimum
MIN_POLL_DELAY_SECS = 0

# if true, mocks the NCBI blast request process and returns a canned result
MOCK_BLAST = False

# if MOCK_BLAST and MOCK_BLAST_HAS_RESULTS are true, returns a canned file with hits;
# otherwise, returns a canned file with no hits
MOCK_BLAST_HAS_RESULTS = True

# parameters passed to the API during a query; note that these can significantly affect runtime
# and the quality of your results
BLAST_PARAMS = {
    'WORD_SIZE': '7',
    'EXPECT': '1000',
    'HITLIST_SIZE': '100',
    'MATCH_SCORES': '1,-3',
    'NUCL_REWARD': '1',
    'NUCL_PENALTY': '-3',
    'GAPCOSTS': '5 2',

    'FILTER': 'F'
}

# if true, expects taxon data from the taxdump file (obtained from ftp://ftp.ncbi.nih.gov/pub/taxonomy/) to be
# extracted to a folder named ./data, and loads taxon info from those files into Taxon and TaxonName.
# the taxon data is currently unused, so it's recommended to leave this flag as false.
LOAD_TAXON_DATA = False


# -----------------------------------
# --- Caching
# -----------------------------------

# enables caching of BLAST results for the same sequence, db, and database
USE_BLAST_CACHING = True

# enables google image search result caching
USE_GIS_CACHING = True
