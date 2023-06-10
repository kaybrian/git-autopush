import os
import subprocess
import time

from git import Repo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class GitEventHandler(FileSystemEventHandler):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo

    def on_modified(self, event):
        self.process_event(event)

    def on_created(self, event):
        self.process_event(event)

    def on_deleted(self, event):
        self.process_event(event)

    def process_event(self, event):
        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            self.perform_git_operations(file_path)

    def perform_git_operations(self, file_path):
        # Add the file
        self.repo.index.add([file_path])

        # Get the filename without the path
        filename = os.path.basename(file_path)

        # Construct the commit message
        commit_message = f"Updated {filename}"

        # Commit the changes with the specific message
        self.repo.index.commit(commit_message)

        # Push the changes
        self.repo.remote().push()


def monitor_directory(directory):
    repo = Repo(directory)
    event_handler = GitEventHandler(repo)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    directory = os.path.dirname(os.path.realpath(__file__))
    monitor_directory(directory)
