"""
CPU Maxer Prank (Windows)
--------------------------
Silently maxes out all CPU cores to make the PC genuinely slow.
No console window when run as .pyw

HOW TO RUN:
  - Double-click slowpc_prank.pyw  (silent, no window)
  - Auto-stops after PRANK_DURATION_MINUTES

TO STOP EARLY:
  - Open Task Manager > find "pythonw.exe" > End Task
"""

import threading
import time
import os
import multiprocessing

# ── CONFIG ──────────────────────────────────────────────────────
PRANK_DURATION_MINUTES = 10   # Auto-stops after this long
# ────────────────────────────────────────────────────────────────

_stop_event = threading.Event()

def burn_core():
    """Pegs a single CPU core at 100%."""
    while not _stop_event.is_set():
        _ = 99999 * 99999  # Pure busy loop

def main():
    num_cores = os.cpu_count() or 4  # One thread per logical core

    threads = []
    for _ in range(num_cores):
        t = threading.Thread(target=burn_core, daemon=True)
        t.start()
        threads.append(t)

    # Auto-stop after time limit
    _stop_event.wait(timeout=PRANK_DURATION_MINUTES * 60)
    _stop_event.set()

if __name__ == "__main__":
    main()
