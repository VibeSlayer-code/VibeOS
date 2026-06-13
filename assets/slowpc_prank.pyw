"""
PC Slow Prank Script (Windows)
-------------------------------
Simulates a lagging, freezing, slow PC using three effects:
  1. Mouse jitter & input lag
  2. Periodic CPU spikes (real slowdown)
  3. Sudden freeze bursts (mouse locks up)

HOW TO RUN:
  - Make sure Python + pyautogui is installed:
      pip install pyautogui
  - Double-click the .pyw file (no console window will appear)
  - OR run: pythonw slowpc_prank.pyw

SECRET KILL SWITCH:
  - Move your mouse to the TOP-LEFT corner of the screen (0, 0) to stop it
  - OR it auto-stops after PRANK_DURATION_MINUTES (default: 10 min)

TIPS:
  - Best used when brother is browsing, gaming, or watching something
  - Don't use while he has unsaved work (CPU spike may cause real slowness)
"""

import pyautogui
import threading
import time
import random
import sys

# ─── CONFIG ────────────────────────────────────────────────────────────────────

PRANK_DURATION_MINUTES = 10        # Auto-stop after this many minutes

# Mouse lag settings
MOUSE_JITTER_AMOUNT   = 4          # Max pixels of jitter (higher = more annoying)
MOUSE_JITTER_INTERVAL = (0.08, 0.18)  # Seconds between jitter ticks

# CPU spike settings
CPU_SPIKE_EVERY       = (20, 50)   # Random interval (seconds) between spikes
CPU_SPIKE_DURATION    = (4, 9)     # How long each spike lasts (seconds)
CPU_SPIKE_THREADS     = (3, 6)     # How many threads to spin up per spike

# Freeze settings
FREEZE_EVERY          = (40, 120)  # Random interval (seconds) between freezes
FREEZE_DURATION       = (2, 5)     # How long each freeze lasts (seconds)

# ───────────────────────────────────────────────────────────────────────────────

pyautogui.FAILSAFE = False  # Disable pyautogui's corner-stop (we do our own)

_running = True
_lock    = threading.Lock()
_freeze  = False  # When True, freeze thread locks the mouse


def set_running(val):
    global _running
    with _lock:
        _running = val


def is_running():
    with _lock:
        return _running


def set_freeze(val):
    global _freeze
    with _lock:
        _freeze = val


def is_frozen():
    with _lock:
        return _freeze


# ─── EFFECT 1: Mouse jitter / input lag ────────────────────────────────────────

def mouse_lag_thread():
    """Adds tiny random jitter to the cursor, making it feel laggy and unresponsive."""
    while is_running():
        try:
            if not is_frozen():
                x, y = pyautogui.position()
                # Skip jitter if already in kill-switch corner
                if x < 10 and y < 10:
                    set_running(False)
                    return

                jx = random.randint(-MOUSE_JITTER_AMOUNT, MOUSE_JITTER_AMOUNT)
                jy = random.randint(-MOUSE_JITTER_AMOUNT, MOUSE_JITTER_AMOUNT)
                pyautogui.moveTo(x + jx, y + jy, duration=0)

            sleep_time = random.uniform(*MOUSE_JITTER_INTERVAL)
            time.sleep(sleep_time)

        except Exception:
            time.sleep(0.1)


# ─── EFFECT 2: CPU spikes ───────────────────────────────────────────────────────

def cpu_spike_thread():
    """Periodically burns CPU to create real performance drops."""
    while is_running():
        wait = random.uniform(*CPU_SPIKE_EVERY)
        # Sleep in small chunks so we can react to kill signal quickly
        for _ in range(int(wait * 10)):
            if not is_running():
                return
            time.sleep(0.1)

        if not is_running():
            return

        duration    = random.uniform(*CPU_SPIKE_DURATION)
        num_threads = random.randint(*CPU_SPIKE_THREADS)
        end_time    = time.time() + duration

        def burn_cpu():
            # Busy loop — genuinely stresses the CPU
            while time.time() < end_time and is_running():
                _ = sum(i * i for i in range(5000))

        spike_threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=burn_cpu, daemon=True)
            t.start()
            spike_threads.append(t)

        for t in spike_threads:
            t.join()


# ─── EFFECT 3: Sudden freeze ────────────────────────────────────────────────────

def freeze_thread():
    """Occasionally locks the mouse in place, simulating a full system freeze."""
    while is_running():
        wait = random.uniform(*FREEZE_EVERY)
        for _ in range(int(wait * 10)):
            if not is_running():
                return
            time.sleep(0.1)

        if not is_running():
            return

        # Snap to current position and hold there
        freeze_dur = random.uniform(*FREEZE_DURATION)
        fx, fy    = pyautogui.position()
        set_freeze(True)
        end_time  = time.time() + freeze_dur

        while time.time() < end_time and is_running():
            try:
                pyautogui.moveTo(fx, fy, duration=0)
            except Exception:
                pass
            time.sleep(0.01)

        set_freeze(False)


# ─── WATCHDOG: Auto-stop after time limit ──────────────────────────────────────

def watchdog_thread():
    """Stops the prank after PRANK_DURATION_MINUTES automatically."""
    total_seconds = PRANK_DURATION_MINUTES * 60
    for _ in range(int(total_seconds * 10)):
        if not is_running():
            return
        time.sleep(0.1)
    set_running(False)


# ─── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    effects = [
        threading.Thread(target=mouse_lag_thread,  daemon=True, name="MouseLag"),
        threading.Thread(target=cpu_spike_thread,  daemon=True, name="CpuSpike"),
        threading.Thread(target=freeze_thread,     daemon=True, name="Freeze"),
        threading.Thread(target=watchdog_thread,   daemon=True, name="Watchdog"),
    ]

    for t in effects:
        t.start()

    # Keep main thread alive until killed
    while is_running():
        time.sleep(0.5)

    # Give threads a moment to wind down
    time.sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
