import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

watched_folder = input("Target path: ")
clone_destination = rf"Results"

class Watcher:
    def __init__(self, watched_folder, clone_destination):
        self.observer = Observer()
        self.watched_folder = watched_folder
        self.clone_destination = clone_destination

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watched_folder, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print("Received created event - %s." % event.src_path)
            if os.path.isdir(event.src_path):
                shutil.copytree(event.src_path, os.path.join(clone_destination, os.path.basename(event.src_path)))
            else:
                shutil.copy2(event.src_path, clone_destination)
            print("Cloned %s to %s." % (event.src_path, clone_destination))

if __name__ == '__main__':
    w = Watcher(watched_folder, clone_destination)
    w.run()
