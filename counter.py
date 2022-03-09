# THE GEIGER COUNTER (at last)

import time
import datetime
import RPi.GPIO as GPIO
from collections import deque

GPIO.setmode(GPIO.BOARD)
millis = lambda: int(round(time.time() * 1000))

counts = deque()
usvh_ratio = 0.00812037037037 # This is for the J305 tube
#usvh_ratio = 0.00277 # This is for the SBM20 tube

# This method fires on edge detection (the pulse from the counter board)
def countme(channel):
    global counts
    timestamp = datetime.datetime.now()
    counts.append(timestamp)

# Set the input with falling edge detection for geiger counter pulses
GPIO.setup(7, GPIO.IN)
GPIO.add_event_detect(7, GPIO.FALLING, callback=countme)

loop_count = 0

# In order to calculate CPM we need to store a rolling count of events in the last 60 seconds
# This loop runs every second to update the Nixie display and removes elements from the queue
# that are older than 60 seconds
while True:
    loop_count = loop_count + 1

    try:
        while counts[0] < datetime.datetime.now() - datetime.timedelta(seconds=60):
            counts.popleft()
    except IndexError:
        pass # there are no records in the queue.

    if loop_count == 10:
        print(int(len(counts)))
        print("{:.2f}".format(len(counts)*usvh_ratio))
        loop_count = 0

    text_count = f"{len(counts):0>3}"
    print(text_count)

    # Update the displays
    line1 = "uSv/h: {:.2f}   ".format(len(counts)*usvh_ratio)
    line2 = "CPM: {}    ".format(int(len(counts)))
    print(line1)
    print(line2)

    time.sleep(1)
