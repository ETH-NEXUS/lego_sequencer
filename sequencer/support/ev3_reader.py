import random
import socket
import rpyc

from time import sleep
from ..default_settings import MOCK_COMM, TIME_MOD

COLORS = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
BRICK_DEG = 54
NUM_BRICKS = 28

# conn = rpyc.classic.connect('ev3dev.local')
# ev3 = conn.modules['ev3dev.ev3']
g_conn = None
g_ev3 = None


class FatalDisconnectException(Exception):
    pass


def get_connection():
    global g_conn, g_ev3
    fail_count = 0

    while fail_count < 3:
        try:
            g_ev3.Sound.beep()
            return g_conn, g_ev3
        except (AttributeError, socket.gaierror):
            # increment the fail counter and try again, up to a max of 3 times
            fail_count += 1
            g_conn = rpyc.classic.connect('ev3dev.local')
            g_ev3 = g_conn.modules['ev3dev.ev3']

    raise FatalDisconnectException("Disconnected and ran out of reconnect attempts")


def nudge(direction, amount=1):
    conn, ev3 = get_connection()
    m = ev3.LargeMotor('outD')

    nudge_amount = (BRICK_DEG if direction == 'right' else -BRICK_DEG) * amount
    m.run_to_rel_pos(position_sp=nudge_amount, speed_sp=900, stop_action="hold")

    return {'msg': 'nudged %s degrees' % nudge_amount}


def query_sequencer():
    try:
        conn, ev3 = get_connection()
    except FatalDisconnectException:
        return {'error': "Disconnected and couldn't recover the connection"}

    m = ev3.LargeMotor('outD')
    sign_m = ev3.Motor('outC')
    cl = ev3.ColorSensor()
    lcd = ev3.Screen()

    # Put the color sensor into COL-COLOR mode.
    cl.mode = 'COL-COLOR'

    # start producing readings until we reach a white
    counted_bricks = 0
    last_value = COLORS[cl.value()]
    for idx in range(NUM_BRICKS):
        sleep(0.1)

        # spin the sign 180 degrees per read
        sign_m.run_to_rel_pos(position_sp=180, speed_sp=900)

        yield {
            'brick_id': counted_bricks,
            'color': COLORS[cl.value()]
        }
        counted_bricks += 1

        m.run_to_rel_pos(position_sp=-BRICK_DEG, speed_sp=200, stop_action="hold")
        m.wait_while('running')

    # rewind back to white
    m.run_to_rel_pos(position_sp=BRICK_DEG * NUM_BRICKS, speed_sp=900, stop_action="hold")


SAMPLE_SEQUENCES = [
    # >ENA|BAA20512|BAA20512.1 Cyprinus carpio (common carp) alpha-globin
    """
    ATGAGTCTCTCTGATAAGGACAAGGCTGCTGTGAAAGCCCTATGGGCTAAGATCAGCCCC
    AAAGCCGATGATATCGGCGCTGAAGCTCTCGGCAGAATGCTGACCGTCTACCCTCAGACC
    AAGACCTACTTCGCTCACTGGGATGACCTGAGCCCTGGGTCCGGTCCTGTGAAGAAGCAT
    GGCAAGGTTATCATGGGTGCAGTGGCCGATGCCGTTTCAAAAATAGACGACCTTGTGGGA
    GGTCTGGCCTCCCTGAGCGAACTTCATGCTTCCAAGCTGCGTGTTGACCCGGCCAACTTC
    AAGATCCTCGCACACAATGTCATCGTGGTCATCGGCATGCTCTTCCCTGGAGACTTCCCC
    CCAGAGGTTCACATGTCAGTTGACAAGTTTTTCCAGAACTTGGCTCTGGCTCTCTCTGAG
    AAGTACCGCTAA""",
    # >ENA|CAA23748|CAA23748.1 Homo sapiens (human) alpha globin
    """
    ATGGTGCTGTCTCCTGCCGACAAGACCAACGTCAAGGCCGCCTGGGGTAAGGTCGGCGCG
    CACGCTGGCGAGTATGGTGCGGAGGCCCTGGAGAGGATGTTCCTGTCCTTCCCCACCACC
    AAGACCTACTTCCCGCACTTCGACCTGAGCCACGGCTCTGCCCAAGTTAAGGGCCACGGC
    AAGAAGGTGGCCGACGCGCTGACCAACGCCGTGGCGCACGTGGACGACATGCCCAACGCG
    CTGTCCGCCCTGAGCGACCTGCACGCGCACAAGCTTCGGGTGGACCCGGTCAACTTCAAG
    CTCCTAAGCCACTGCCTGCTGGTGACCCTGGCCGCCCACCTCCCCGCCGAGTTCACCCCT
    GCGGTGCACGCTTCCCTGGACAAGTTCCTGGCTTCTGTGAGCACCGTGCTGACCTCCAAA
    TACCGTTAA""",
    # >ENA|CAA24095|CAA24095.1 Mus musculus (house mouse) alpha-globin
    """ATGGTGCTCTCTGGGGAAGACAAAAGCAACATCAAGGCTGCCTGGGGGAAGATTGGTGGC
    CATGGTGCTGAATATGGAGCTGAAGCCCTGGAAAGGATGTTTGCTAGCTTCCCCACCACC
    AAGACCTACTTTCCTCACTTTGATGTAAGCCACGGCTCTGCCCAGGTCAAGGGTCACGGC
    AAGAAGGTCGCCGATGCGCTGGCCAGTGCTGCAGGCCACCTCGATGACCTGCCCGGTGCC
    TTGTCTGCTCTGAGCGACCTGCATGCCCACAAGCTGCGTGTGGATCCCGTCAACTTCAAG
    CTCCTGAGCCACTGCCTGCTGGTGACCTTGGCTAGCCACCACCCTGCCGATTTCACCCCC
    GCGGTACATGCCTCTCTGGACAAATTCCTTGCCTCTGTGAGCACCGTGCTGACCTCCAAG
    TACCGTTAA""",
    # >ENA|CAA28435|CAA28435.1 Capra hircus (goat) alpha-globin
    """ATGTCTCTGACCAGGACTGAGAGGACCATCATCCTGTCCCTGTGGAGCAAGATCTCCACA
    CAGGCAGACGTCATTGGCACCGAGACCCTGGAGAGGCTCTTCTCCTGCTACCCGCAGGCC
    AAGACCTACTTCCCGCACTTCGACCTGCACTCGGGCTCCGCGCAGCTGCGCGCGCACGGC
    TCCAAGGTGGTGGCCGCCGTGGGCGACGCGGTCAAGAGCATCGACAACGTGACGAGCGCG
    CTGTCCAAGCTGAGCGAGCTGCACGCCTACGTGCTGCGCGTGGACCCGGTCAACTTCAAG
    TTCCTGTCCCACTGCCTGCTGGTCACGTTGGCCTCGCACTTCCCCGCCGACTTCACGGCC
    GACGCGCACGCCGCCTGGGACAAGTTCCTGTCCATCGTGTCCGGCGTCCTGACGGAGAAG
    TACCGCTGA"""
]

BASE_TO_COL = {
    'A': 'green',
    'C': 'blue',
    'T': 'red',
    'G': 'yellow'
}

USE_GARBAGE_SEQ = False
GARBAGE_SEQ = """ATGTCCAGGAGAGATAGAGGACCATCCGGACCAGGAGAGGACCATCACTG"""


def query_sequencer_mock():
    counted_bricks = 0
    cl_value = 6 # white
    last_value = COLORS[cl_value]

    # randomly choose one of our sequences
    # add whitespace adapters to the beginning and end
    src_seq = random.choice(SAMPLE_SEQUENCES) if not USE_GARBAGE_SEQ else GARBAGE_SEQ
    seq = (
        (['white'] * 3) +
        list(map(lambda x: BASE_TO_COL[x], "".join(src_seq.split())[:(NUM_BRICKS - 6)]))
        + (['white'] * 3)
    )

    for idx in range(NUM_BRICKS):
        cl_color = seq[idx]

        sleep(0.1 * TIME_MOD)

        yield {
            'brick_id': counted_bricks,
            'color': cl_color
        }
        counted_bricks += 1
        sleep(0.2 * TIME_MOD)


def query_full_sequence():
    seq_func = query_sequencer_mock if MOCK_COMM else query_sequencer

    for x in seq_func():
        yield x
