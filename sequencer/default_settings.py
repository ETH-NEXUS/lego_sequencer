# -----------------------------------
# --- LEGO Sequencer Mocking
# -----------------------------------

# if true, mocks communication with the LEGO brick, producing sequences from real organisms
# (see support.ev3_reader.SAMPLE_SEQUENCES for details)
MOCK_COMM = False
# if MOCK_COMM=True, the mock process duration is multiplied by this value (>1.0 slower, <1.0 faster)
TIME_MOD = 0.5


# -----------------------------------
# --- NCBI BLAST Mocking:
# -----------------------------------

# if true, mocks the NCBI blast request process and returns a canned result
MOCK_BLAST = False
# if MOCK_BLAST and MOCK_BLAST_HAS_RESULTS are true, returns a canned file with hits;
# otherwise, returns a canned file with no hits
MOCK_BLAST_HAS_RESULTS = True
