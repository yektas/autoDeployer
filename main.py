import os
import time
from datetime import datetime

import configparser
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from utils import scp


config = configparser.ConfigParser()
config.read("config.properties")
remotePath = config["SETTINGS"]["toCopyPath"]
localPath = config["SETTINGS"]["fromCopyPath"]

old = 0


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        global old
        if event.event_type == 'modified':
            file = event.src_path
            if file.endswith(".jar"):
                file_name = os.path.basename(file)
                statbuf = os.stat(file)
                new = statbuf.st_mtime
                if (new - old) > 0.5:
                    print("{} has changed, deploying now... {}".format(file_name, datetime.now()))
                    scp(file, remotePath + "/{}".format(file_name))
                old = new


if __name__ == "__main__":

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=localPath,
                      recursive=False)

    observer.start()
    print("Waiting for a change to happen...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
