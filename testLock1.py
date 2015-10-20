"""
import portalocker
import time

with portalocker.Lock('text.txt', timeout=5) as fh:
    time.sleep(3)
    fh.write("Sono in testLock1.py")
"""
from lockfile import LockFile
import time

lock = LockFile('text.txt')
with lock:
    print lock.path, 'is locked.'
    time.sleep(3)
    with open('text.txt', "w") as file:
        file.write("Sono in testLock1.py dopo sleep\n")
