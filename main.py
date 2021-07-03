import time
import RPi.GPIO as GPIO
import sys

# table

# E T A I O N S H R D U L C M F W Y G P B V K Q J X Z
# table: https://media.discordapp.net/attachments/530622307383771156/860751907038560276/unknown.png?width=769&height=484


# order is 01, 10, 11

tree = [ '?', # top level
        ['e', # e level
            ['a', 'r', 'd', 'u'], # for leaf nodes, just put the value
            ['i', 'l', 'c', 'm'], # or, a list with just that element
            ['o', 'f', 'w', 'y']
        ],
        ['t', # t level 
            ['n', 'g', 'p', 'b'],
            ['s', 'v', 'k', 'q'],
            ['h', 'j', 'x', 'z']
        ],
        [' ', # space level 
            [','],
            ['.'],
            ['\n']
        ]
    ]

currentTree = tree
def processKeystroke(state):
    global currentTree
    left = state[1]
    right = state[0]
    control = state[2]
    if control == 0:
        # generate next node index
        key = right * 2 + left - 1
        # 01 -> 0
        # 10 -> 1
        # 11 -> 2
        # we add one because the data is in the first spot
        currentTree = currentTree[key + 1]
    else:
        # control == 1
        if left == 0 or right == 0:
            print "Not sure what to do with " + str(state)
        node = currentTree # the current node
        if type(node) == type([]):
            sys.stdout.write(node[0])
        else:
            sys.stdout.write(node)
        sys.stdout.flush()
        currentTree = tree

GPIO.setmode(GPIO.BCM)



def setup(x):
    GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



one = 16
two = 20
three = 21

setup(one)
setup(two)
setup(three)

lastState = [0, 0, 0]

try:
    while True:
        time.sleep(0.01)
        state = [GPIO.input(x) for x in [one, two, three]]
        if state == lastState:
            continue
        for n in range(0, 3):
            if state[n] > lastState[n]:
                lastState[n] = 1
        if sum(state) == 0 and sum(lastState) > 0:
            # print(lastState[0] * 4 + lastState[1] * 2 + lastState[2])
            processKeystroke(lastState)
            lastState = [0, 0, 0]
except KeyboardInterrupt:
    pass

GPIO.cleanup()
