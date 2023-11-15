import threading
import time
from datetime import datetime, timedelta
import io
from contextlib import redirect_stdout
import IPython

d = {"n": 0}
end = True
current_time = 0

def test(f, debug=False):
    """ Test correctness and speed of the implementation """
    tests = [
        ([1, 1, 1], 2),
        ([2, 1, 1], 1),
        ([1, 3, 5, 8, 9, 2, 6, 7, 6, 8, 9], 3),
        ([2, 3, 1, 1, 4], 2),
        ([5]*51, 10)
    ]
    
    failed_count = 0 # Number of failed test (logical or time)
    failed_time_count = 0 # Number of failed test due to time
    for arr, out in tests:
        
        res = []
        t = threading.Thread(target=_helper, args=(f, arr,res)) # {res} will be used by the other thread to store the result
        t.start()
        t.join(5) # Kill the thread after 5 seconds
        
        if len(res) == 0:
            failed_time_count += 1
            failed_count += 1
            
        elif res[0] != out:
            failed_count += 1
            if debug:
                print(f'For input : {arr}, expected {out} but got {res[0]}')

    if failed_count > 0:
        print(f"❌ Your implementation failed {failed_count} test(s) out of {len(tests)} tests")
        if failed_time_count > 0:
            print(f"    ❌ {failed_time_count} test was too slow ")
        else:
            print(f"    ✅ but you implementation is fast enough 🚀.")
    else:
        print(f"✅ Your implementation passed every tests and is fast enough 🚀.")
    # trap = io.StringIO()
    # with redirect_stdout(trap):
    now = datetime.now() + timedelta(hours=1)
    log(failed_count, failed_time_count, now)

        
def _helper(f, arr, res):
    """ Helper with mutable {res} variable to get result at the end of multithreading """
    res.append(f(arr))

def due_time():
    global end
    global current_time
    if (end and not current_time):
        now = datetime.now()
        due_time = now + timedelta(minutes=10) + timedelta(hours=1)
        current_time = due_time.strftime("%H:%M:%S")
        end = False
        print(f"Please upload this notebook on Moodle by {current_time}.")
    else:
        print(f"Please upload this notebook on Moodle by {current_time}.")
    

def log(failed_count, failed_time_count, test_time):
    global d
    d["n"] += 1
    d[d["n"]] = {}
    d[d["n"]]["fcount"] = failed_count
    d[d["n"]]["ftime"] = failed_time_count
    d[d["n"]]["time"] = test_time
    # print(d)
    dbis = {"hello" : "1"}
    IPython.display.HTML("<br>", metadata=dbis)
    # store = IPython.get_ipython().find_line_magic('store')
    # store('d')

