# -----------------------------------
# --- LEGO Sequencer Mocking
# -----------------------------------

# if true, mocks communication with the LEGO brick, producing sequences from real organisms
# (see support.ev3_reader.SAMPLE_SEQUENCES for details)
MOCK_COMM = False

# if MOCK_COMM=True, the mock process duration is multiplied by this value (>1.0 slower, <1.0 faster)
TIME_MOD = 0.1

# if USE_RANDOM_SEQ=True, uses a random sequence of {A,C,T,G} instead of a sample sequence
# (note that this will often not return anything and take a long time doing it)
USE_RANDOM_SEQ = True


# -----------------------------------
# --- NCBI BLAST:
# -----------------------------------

# time in seconds before the BLAST request times out, never if None
BLAST_TIMEOUT = 120

# if true, mocks the NCBI blast request process and returns a canned result
MOCK_BLAST = False

# if MOCK_BLAST and MOCK_BLAST_HAS_RESULTS are true, returns a canned file with hits;
# otherwise, returns a canned file with no hits
MOCK_BLAST_HAS_RESULTS = True


# -----------------------------------
# --- Caching
# -----------------------------------

# enables caching of BLAST results for the same sequence, db, and database
USE_BLAST_CACHING = True

# enables google image search result caching
USE_GIS_CACHING = True
