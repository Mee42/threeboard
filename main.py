import time
import RPi.GPIO as GPIO
import sys

# table

# E T A I O N S H R D U L C M F W Y G P B V K Q J X Z
# table: https://media.discordapp.net/attachments/530622307383771156/860751907038560276/unknown.png?width=769&height=484

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

currentTree = {}
currentModifiers = [] # contains one of the below keys

shiftKey = { 'key': 'shift' } # these are symbols. Mainly used for object equality
ctrlKey  = { 'key': 'ctrl'  }
altKey   = { 'key': 'alt'   }     
winKey   = { 'key': 'win'   }
capsKey  = { 'key': 'caps'  }

logFile = open('log.log', 'a')
def log(s):
    global logFile
    logFile.write(str(s))
    logFile.flush()

log('\n\n\n\n\n\n\n    ----    program start    ----\n')
# runs f, then resets the tree to the top.
def doThenReset(f):
    def doThenResetN():
        global tree
        global currentTree
        f()
        currentTree = tree
    return doThenResetN

def addModifier(mod):
    def addModifierN():
        global currentModifiers
        global tree
        global currentTree
        log('+' + mod['key'] + ' ')
        currentModifiers.append(mod)
        if mod == shiftKey and capsKey in currentModifiers:
            currentModifiers.remove(capsKey)
        currentTree = tree
    return addModifierN

def error(str):
    raise RuntimeError(str)


# order is [selector, 01, 10, 11, 001, 01, 10]. 
# if the node traversed to is a function, it's evaluated immediately
# if 'None' is selected, an error will be printed with information (somewhere)
tree = ['', # top level. Don't print anything if it's empty
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
        ],
        [ None, # 001 combination.
            addModifier(shiftKey), #  01. no subthings cause it 
            addModifier(ctrlKey),
            addModifier(altKey),
            [ None, # the next level nested
                addModifier(capsKey), 
                addModifier(winKey)
            ]
        ]
    ]

currentTree = tree
def processKeystroke(state):
    global currentTree
    global currentShift
    global currentModifiers
    stateStr = str(state[0]) + str(state[1]) + str(state[2])
    log(stateStr + " ")
    if state == [1, 1, 1]: # if we are in 'input' mode
        node = currentTree # the current node
        value = node
        if type(node) == type([]): 
            # if it's a list, like ['n', 'g', 'p', 'b'], then take the first element
            value = node[0]
        # uppercase if the shift modifier has been activated
        if value != "" and (shiftKey in currentModifiers or capsKey in currentModifiers):
            if value in lowercase:
                value = uppercase[lowercase.index(value)]
        sys.stdout.write(value)
        sys.stdout.flush()
        currentTree = tree
        if capsKey in currentModifiers:
            currentModifiers = [capsKey] # preserve
        else:
            currentModifiers = []
        log(value + '\n')
    else:
        # the default, look at the tree
        # generate next node index
        key = {
                '010': 0,
                '100': 1,
                '110': 2,
                '001': 3,
                '011': 4,
                '101': 5
            }[stateStr]
        # 010 -> 0
        # 100 -> 1
        # 110 -> 2
        # 001 -> 3
        # 011 -> 4
        # 101 -> 5
        # we add one because the data is in the first spot
        nextNode = currentTree[key + 1]
        if type(nextNode) == type(lambda x: True): # if it's a function
            nextNode() # trust it to set up state
        else: 
            currentTree = nextNode
    

GPIO.setmode(GPIO.BCM)



def setup(x):
    GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def setupout(x):
    GPIO.setup(x, GPIO.OUT)

one = 16
two = 20
three = 21

setup(one)
setup(two)
setup(three)

shiftPin = 12
stickyPin = 6
setupout(shiftPin)


def setStatusLeds():
    GPIO.output(shiftPin, GPIO.HIGH if shiftKey in currentModifiers or capsKey in currentModifiers else GPIO.LOW)

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
            try:
                processKeystroke(lastState)
            except Exception as e:
                log("ERROR: " + str(e) + "\n")
            setStatusLeds()
            lastState = [0, 0, 0]
except KeyboardInterrupt:
    pass

log('exited')
GPIO.cleanup()
logFile.close()







