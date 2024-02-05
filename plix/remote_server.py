import sys
import time
import os
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SpecificFileEventHandler(FileSystemEventHandler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.last_modified = time.time()

    def on_modified(self, event):
        current_time = time.time()
        if not event.is_directory and event.src_path.endswith(self.filename) and current_time - self.last_modified > 1:  # 1 second debounce
            self.last_modified = current_time
            logging.info(f'File {self.filename} modified. Rerunning it.')
            file_changed_action(self.filename)

def file_changed_action(filename):
    python_interpreter = 'python'
    script_path = filename

    os.environ['RUNNING_FROM_WATCHDOG'] = '1'
    print('Running the script')
    subprocess.run([python_interpreter, script_path])
    del os.environ['RUNNING_FROM_WATCHDOG']

def run_watchdog():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    file_to_monitor = sys.argv[0]

    logging.info(f'Starting to watch the file {file_to_monitor} in directory {path!r}')

    event_handler = SpecificFileEventHandler(file_to_monitor)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
