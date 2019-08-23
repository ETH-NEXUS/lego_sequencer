import socket
import rpyc
from time import sleep

COLORS = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
BRICK_DEG = 54
NUM_BRICKS = 26

# conn = rpyc.classic.connect('ev3dev.local')
# ev3 = conn.modules['ev3dev.ev3']
conn = None
ev3 = None


class FatalDisconnectException(Exception):
    pass


def query_sequencer():
    global conn, ev3

    # every time we run it, start the connection
    # FIXME: can we somehow reconnect if it's not available?

    fail_count = 0
    success = False

    try:
        while not success:
            try:
                ev3.Sound.beep()
                success = True
            except (AttributeError, socket.gaierror):
                # increment the fail counter and try again, up to a max of 3 times
                fail_count += 1
                conn = rpyc.classic.connect('ev3dev.local')
                ev3 = conn.modules['ev3dev.ev3']

                if fail_count > 3:
                    raise FatalDisconnectException("Disconnected and couldn't recover")

    except FatalDisconnectException:
        return {'error': "Disconnected and couldn't recover the connection"}

    m = ev3.LargeMotor()
    cl = ev3.ColorSensor()

    # Put the color sensor into COL-COLOR mode.
    cl.mode = 'COL-COLOR'

    # start producing readings until we reach a white
    readings = []
    counted_bricks = 0
    last_value = COLORS[cl.value()]
    for idx in range(NUM_BRICKS):
        m.run_to_rel_pos(position_sp=-BRICK_DEG, speed_sp=200, stop_action="hold")

        sleep(0.1)
        readings.append({
            'brick_id': counted_bricks,
            'color': COLORS[cl.value()]
        })
        counted_bricks += 1
        sleep(0.2)

    # rewind back to white
    m.run_to_rel_pos(position_sp=BRICK_DEG * NUM_BRICKS, speed_sp=900, stop_action="hold")

    return readings
