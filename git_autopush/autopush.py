import os
import time
import subprocess
from pyinotify import WatchManager, ProcessEvent, Notifier, IN_CREATE, IN_MODIFY, IN_DELETE

class FileMonitor(ProcessEvent):
    def __init__(self):
        self.path = os.getcwd()  # Get the current working directory
        self.files = {}
        self.wm = WatchManager()
        self.mask = IN_CREATE | IN_MODIFY | IN_DELETE
        self.wm.add_watch(self.path, self.mask)

    def process_default(self, event):
        if event.pathname.startswith(self.path):
            self.check_files()

    def check_files(self):
        current_files = {
            filename: os.stat(filename).st_mtime
            for filename in os.listdir(self.path)
        }

        added_files = current_files.keys() - self.files.keys()
        deleted_files = self.files.keys() - current_files.keys()
        modified_files = {
            filename for filename in self.files.keys() & current_files.keys()
            if self.files[filename] != current_files[filename]
        }

        for file in added_files:
            commit_message = f"Created {file}"
            add_and_push(file, commit_message)

        for file in deleted_files:
            commit_message = f"Deleted {file}"
            add_and_push(file, commit_message)

        for file in modified_files:
            commit_message = f"Updated {file}"
            add_and_push(file, commit_message)

        self.files = current_files

def monitor_directory():
    path = os.getcwd()  # Get the current working directory
    if not os.path.exists(os.path.join(path, ".git")):
        print("Directory is not a git repo!")
        return

    wm = WatchManager()
    mask = IN_CREATE | IN_MODIFY | IN_DELETE
    notifier = None

    try:
        notifier = Notifier(wm, FileMonitor())
        wdd = wm.add_watch(path, mask, rec=True)
        print("Monitoring directory...")

        while True:
            try:
                notifier.process_events()
                if notifier.check_events():
                    notifier.read_events()
            except KeyboardInterrupt:
                notifier.stop()
                break

            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if notifier is not None:
            notifier.stop()

def add_and_push(file, commit_message):
    subprocess.run(["git", "add", file])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    monitor_directory()
