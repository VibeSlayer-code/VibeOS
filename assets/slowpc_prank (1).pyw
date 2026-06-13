import threading
import time
import os

_stop = threading.Event()

def burn():
    while not _stop.is_set():
        _ = sum(i * i for i in range(100000))

def main():
    # 2x core count threads = very heavy CPU saturation
    num_threads = (os.cpu_count() or 4) * 2

    for _ in range(num_threads):
        t = threading.Thread(target=burn, daemon=True)
        t.start()

    # Runs until killed — open Task Manager > End Task on "pythonw.exe"
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
