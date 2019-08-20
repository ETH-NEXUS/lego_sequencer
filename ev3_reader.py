import rpyc
from time import sleep

conn = rpyc.classic.connect('ev3dev.local')
ev3 = conn.modules['ev3dev.ev3']

COLORS = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
BRICK_DEG = 54
NUM_BRICKS = 26


def query_sequencer():
    m = ev3.LargeMotor()
    cl = ev3.ColorSensor()

    # Put the color sensor into COL-COLOR mode.
    cl.mode = 'COL-COLOR'

    # # reset position before we start reading
    # kill_switch = 0
    # last_value = cl.value()
    # while last_value != 'white' or kill_switch > 100:
    #     last_value = cl.value()
    #     print(last_value)
    #     m.run_to_rel_pos(position_sp=60, speed_sp=100, stop_action="hold")
    #     kill_switch += 1
    #     sleep(0.1)

    # 1. read to the white position
    # 2. start translating until we reach another white region
    # 3. go back to previous white region

    # move ahead to the first non-white region
    # last_value = cl.value()
    # while last_value == 'white' or last_value == 'unknown':
    #     last_value = cl.value()
    #     m.run_to_rel_pos(position_sp=60, speed_sp=300, stop_action="hold")
    #     sleep(0.5)

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
