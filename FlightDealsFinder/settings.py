import sys
import time
import threading
from contextlib import contextmanager

def animate_dots(stop_event, message):
    while not stop_event.is_set():
        for dots in range(4):  # Animate 0 to 3 dots
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r{message}" + "." * dots + "   ")
            sys.stdout.flush()
            time.sleep(0.3)
    sys.stdout.write(f"\r{message}... Done!   \n")
    sys.stdout.flush()

@contextmanager
def animate_loading(message):
    """Context manager to run animate_dots in a background thread while executing a block."""
    stop_event = threading.Event()
    thread = threading.Thread(target=animate_dots, args=(stop_event, message), daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop_event.set()
        thread.join()

def logo():
    logo = """            
            ___________
    =  = ==(___________) \033[1;34;40mFlight Deal Finder\033[0m
                \\_____\\___________________,-~~~~~~~`-.._
                /     o O o o o o O O o o o o o o O o  |\\_
                `~-.__        ___..----..                  )
                      `---~~\\___________/------------`````
                      =  ===(_________D"""
    print(logo)