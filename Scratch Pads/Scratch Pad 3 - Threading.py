
## working threading script from tutorials point

import threading
import time


def print_time(thread_name, delay):
    count = 0

    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (thread_name, time.ctime(time.time())))

try:
    threading._start_new_thread(print_time, ("Thread-1", 2, ))
    threading._start_new_thread(print_time, ("Thread-2", 4, ))

except Exception as e:
    print(e)
    print("Error: unable to start thread")

while 1:
    pass
