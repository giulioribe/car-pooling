"""import portalocker

with portalocker.Lock('text.txt', timeout=5) as fh:
    fh.write("Sono in testLoxk2.py")
"""
from lockfile import LockFile

lock = LockFile('text.txt')
with lock:
    print lock.path, 'is locked.'
    with open('text.txt', "a") as file:
        file.write("Sono in testLock2.py")
