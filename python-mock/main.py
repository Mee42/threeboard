import time
import RPi.GPIO as GPIO
import sys


logFile = open('log.log', 'a')
def log(s):
    global logFile
    logFile.write(str(s))
    logFile.flush()

def error(str):
    raise RuntimeError(str)

log('\n\n\n\n\n\n\n    ----    program start    ----\n')




# custom logic
inWord = False

buf = []
# 1 - dit
# 0 - dah

# morse code mode?
# 100 - dit
# 010 - dah
# 001 - end letter
# 001 001 - end word
def processKeystroke(state):
    global inWord
    global buf
    log("state: " + str(state) + "\n")
    if state == [1, 1, 0]:
        buf = []
        inWord = False
    elif state == [0, 1, 1]:
        # backspace?
        sys.stdout.write(chr(8))
        sys.stdout.write(" ")
        sys.stdout.write(chr(8))
        sys.stdout.flush()
    elif state == [1, 0, 0] or state == [0, 1, 0]:
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
    else:
        log("unhandled state: " + str(state) + "\n")
    setStatusLeds(inWord)


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

def onTick():
    pass








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
        onTick()
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







