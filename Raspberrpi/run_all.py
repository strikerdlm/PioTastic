"""
run_all.py - Master launcher for set_client.py and wio_to_meshtastic.py

Usage:
  python run_all.py           # Normal mode, output to console
  python run_all.py --nohup   # No-hangup mode, runs as a background daemon, logs to files

- In --nohup mode, the script will detach from the terminal and keep running after SSH logout.
- All output (stdout and stderr) from both child scripts will be written to log files in the same directory.
- Debug and restart features are preserved in both modes.
"""
import subprocess
import sys
import os
import time
import signal

DEBUG = True  # Set to True for verbose debug output
RESTART_DELAY = 2  # Seconds to wait before restarting a crashed process

# Get the directory of this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to the scripts to run
SET_CLIENT_PATH = os.path.join(SCRIPT_DIR, 'set_client.py')
WIO_TO_MESHTASTIC_PATH = os.path.join(SCRIPT_DIR, 'wio_to_meshtastic.py')

# Use sys.executable to ensure the same Python interpreter is used
python_exec = sys.executable

# Track restart counts
restart_counts = {
    'set_client.py': 0,
    'wio_to_meshtastic.py': 0
}

NOHUP_MODE = '--nohup' in sys.argv

# Prepare log files if in nohup mode
if NOHUP_MODE:
    LOG_DIR = os.path.join(SCRIPT_DIR, 'logs')
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    set_client_log = open(os.path.join(LOG_DIR, 'set_client_stdout.log'), 'a')
    wio_to_meshtastic_log = open(os.path.join(LOG_DIR, 'wio_to_meshtastic_stdout.log'), 'a')
else:
    set_client_log = subprocess.PIPE
    wio_to_meshtastic_log = subprocess.PIPE

def daemonize():
    """Detach process from terminal (UNIX double-fork)."""
    if os.fork() > 0:
        sys.exit(0)  # First parent exits
    os.setsid()
    if os.fork() > 0:
        sys.exit(0)  # Second parent exits
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    # In nohup mode, redirect stdout/stderr to log files
    if NOHUP_MODE:
        sys.stdout = open(os.path.join(LOG_DIR, 'run_all_stdout.log'), 'a')
        sys.stderr = open(os.path.join(LOG_DIR, 'run_all_stderr.log'), 'a')
        os.dup2(sys.stdout.fileno(), 1)
        os.dup2(sys.stderr.fileno(), 2)

if NOHUP_MODE:
    daemonize()
    print('[DEBUG] run_all.py started in NOHUP/daemon mode.')
else:
    print('[DEBUG] run_all.py started in normal (interactive) mode.')

def start_process(script_path, name, log_file):
    if DEBUG:
        print(f'[DEBUG] Starting {name}...')
    proc = subprocess.Popen([
        python_exec, script_path
    ], stdout=log_file, stderr=subprocess.STDOUT, text=True, bufsize=1)
    return proc

# Start both processes initially
set_client_proc = start_process(SET_CLIENT_PATH, 'set_client.py', set_client_log)
wio_to_meshtastic_proc = start_process(WIO_TO_MESHTASTIC_PATH, 'wio_to_meshtastic.py', wio_to_meshtastic_log)

print('Both set_client.py and wio_to_meshtastic.py have been started.')
if NOHUP_MODE:
    print('Logs:')
    print(f'  set_client.py -> {os.path.join(LOG_DIR, "set_client_stdout.log")})')
    print(f'  wio_to_meshtastic.py -> {os.path.join(LOG_DIR, "wio_to_meshtastic_stdout.log")})')
    print('To stop: kill the run_all.py process (see ps aux | grep run_all.py)')
else:
    print('Press Ctrl+C to stop both processes.')

try:
    while True:
        for proc, name, path, log_file in [
            (set_client_proc, 'set_client.py', SET_CLIENT_PATH, set_client_log),
            (wio_to_meshtastic_proc, 'wio_to_meshtastic.py', WIO_TO_MESHTASTIC_PATH, wio_to_meshtastic_log)
        ]:
            if proc.poll() is not None:
                print(f'[DEBUG] Process {name} exited with code {proc.returncode}')
                restart_counts[name] += 1
                print(f'[DEBUG] Restarting {name} (restart count: {restart_counts[name]}) in {RESTART_DELAY} seconds...')
                time.sleep(RESTART_DELAY)
                if name == 'set_client.py':
                    set_client_proc = start_process(path, name, log_file)
                else:
                    wio_to_meshtastic_proc = start_process(path, name, log_file)
                continue
            if not NOHUP_MODE:
                line = proc.stdout.readline()
                if line:
                    print(f'[{name}] {line}', end='')
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nKeyboardInterrupt received. Terminating both processes...')
    set_client_proc.terminate()
    wio_to_meshtastic_proc.terminate()
    set_client_proc.wait()
    wio_to_meshtastic_proc.wait()
    print('Both processes terminated.')
except Exception as e:
    print(f'[FATAL] Exception in run_all.py: {e}')
finally:
    if NOHUP_MODE:
        set_client_log.close()
        wio_to_meshtastic_log.close() 