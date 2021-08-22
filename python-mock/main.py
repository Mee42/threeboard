import time
import RPi.GPIO as GPIO
import sys


# specification

# mode
#   0 - morse
#   1 - modifiers
#   2 - arrow keys
#   3 - 
#   4 - 
#   5 - system

# in every mode:
#  111: reset to mode 0, state reset
#  011: go to next mode
 
# mode 0, morse
#  morse code table is mostly standard

#  100 | dit (dot)
#  010 | dah (dash)
#  001 | finish letter, if a letter is in progress
#  001 | space


# mode 1, modifiers
#  after finishing (110) this returns to mode 0, but the key sent has the specified modifier
#  can be combined. <C-T> would be 100 110(ctrl) 010 110(shift) 010 001(t)

#   100     110 | ctrl 
#   100 100 110 | win
#   010     110 | shift
#   010 010 110 | alt


# mode 2, arrow keys
#   a good way to navigate around with the arrow keys. 110 can be used to make the next keystroke "bigger"

#  100 | left arrow
#  001 | right arrow
#  010 | up arrow
#  101 | down arrow
#  110 100 | ctrl left arrow   | left by word
#  110 001 | ctrl right arrow  | right by word
#  110 010 | ctrl up arrow     | up by paragraph
#  110 101 | ctrl down arrow   | down by paragraph
#  110 110 100 | home          | go to start of line
#  110 110 001 | end           | go to end of line
#  110 110 010 | ctrl home     | go to start of document
#  110 110 101 | ctrl end      | go to the end of document 


# mode 5, system
#   this is where system-specific controls are

# 100 | halt 



logFile = open('log.log', 'a')
def log(s):
    global logFile
    logFile.write(str(s))
    logFile.flush()

def error(str):
    raise RuntimeError(str)

log('\n\n\n\n\n\n\n    ----    program start    ----\n')


# state
mode = 0
# morse code state

inWord = False
buf = []


def processKeystroke(state):
    global mode
    log("mode: " + str(mode) + " state: " + str(state) + "\n")
    if state == [1, 1, 1]:
        mode = 0
        mode0_morse_init()
    if state == [0, 1, 1]:
        # next mode
        mode = mode + 1
        if mode == 0:
            mode0_morse_init()
    else:
        if mode == 0:
            mode0_morse(state)
        elif mode == 1:
            mode1_modifiers(state)
        elif mode == 2:
            mode2_arrows(state)
        elif mode == 5:
            mode5_system(state)
        else:
            error("Can't find mode " + str(mode))

def mode0_morse_init():
    # runs whenever we enter this mode
    global inWord
    global buf
    inWord = False
    buf = []


def mode0_morse(state):
    global inWord
    global buf
    if state == [1, 0, 0] or state == [0, 1, 0]:
        isDit = 1 if state == [1, 0, 0] else 0
        buf.append(isDit)
        inWord = True
    elif state == [0, 0, 1] and buf == []:
        # space
        sys.stdout.write(" ")
        sys.stdout.flush()
    elif state == [0, 0, 1]:
        char = morseLookup(buf)
        buf = []
        if char == None:
            return # can't write obv
        inWord = False
        sys.stdout.write(char)
        sys.stdout.flush()
def mode1_modifiers(state):
    pass
def mode2_arrows(state):
    pass
def mode5_system(state):
    pass

def morseLookup(arr):
    # chonk lookup
    string = reduce(lambda a, b: a + str(b), arr, "")
    log("looking up " + string + "\n")
    if string in morseObj:
        return morseObj[string]
    log("unknown sequence: " + string)
    return None

# a = dit
# b = dah
morseObj = {
        "10": "a",
        "0111": "b",
        "0101": "c",
        "011": "d",
        "1": "e",
        "1101": "f",
        "001": "g",
        "1111": "h",
        "11": "i",
        "1000": "j",
        "010": "k",
        "1011": "l",
        "00": "m",
        "01": "n",
        "000": "o",
        "1001": "p",
        "0010": "q",
        "101": "r",
        "111": "s",
        "0": "t",
        "110": "u",
        "1110": "v",
        "100": "w",
        "0110": "x",
        "0100": "y",
        "0011": "z",
        "10000": "1",
        "11000": "2",
        "11100": "3",
        "11110": "4",
        "11111": "5",
        "01111": "6",
        "00111": "7",
        "00011": "8",
        "00001": "9",
        "00000": "10",
        "101010": ".",
        "001100": ",",
        "000111": ":",
        "110011": ":",
        "100001": "'",
        "011110": "-",
        "01101": "/",
        "01001": "(",
        "010010": ")",
        "101101": "\"",
        "01110": "=",
        "01010": "+",
        "0110": "*",
        "100101": "@",

# special ones
#        aaaaaaaa ERRROR
#        aaaoa    UNDERSTAND
#        oao INVITATION TO TRANSIT
#        aoaaa WAIT
#        aaaoao END OF WORK
#        oaoao STARTING SIGNAL

        
    }








# set up gpio
GPIO.setmode(GPIO.BCM)

one = 16
two = 20
three = 21
statusPin = 12

GPIO.setup(one, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(two, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(three, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(statusPin, GPIO.OUT)

def setStatusLeds(value):
    GPIO.output(statusPin, value)

lastState = [0, 0, 0]

try:
    while True:
        time.sleep(0.001)
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
            lastState = [0, 0, 0]
except KeyboardInterrupt:
    pass

log('exited')
GPIO.cleanup()
logFile.close()







