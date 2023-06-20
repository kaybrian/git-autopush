import os
import time
import subprocess
import signal
import sys
import hashlib
import threading

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[0m"

def monitor_directory(path="."):
    if not os.path.exists(os.path.join(path, ".git")):
        print(f"{RED}Directory is not a Git repo!{WHITE}")
        return

    print(f"{GREEN}Monitoring...{WHITE}")

    files = {}
    deleted_files_set = set()  # Set to track deleted files

    def populate_files():
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                files[full_path] = hash_file(full_path)

    def exit_gracefully(signal, frame):
        print(f"{GREEN}\nGoodbye!{WHITE}")
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)

    change_event = threading.Event()  # Event object to signal changes

    def file_monitor():
        while True:
            current_files = {}

            for root, dirs, filenames in os.walk(path):
                if ".git" in dirs:
                    dirs.remove(".git")  # Skip the .git directory

                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    current_files[full_path] = hash_file(full_path)

            added_files = current_files.keys() - files.keys()
            deleted_files = files.keys() - current_files.keys()
            modified_files = {
                filename for filename in files.keys() & current_files.keys()
                if files[filename] != current_files[filename]
            }

            if added_files or deleted_files or modified_files:
                for file in added_files:
                    commit_message = f"Created {os.path.basename(file)}"
                    add_and_push(file, commit_message)

                for file in deleted_files:
                    if not file.startswith("./.git"):
                        commit_message = f"Deleted {os.path.basename(file)}"
                        delete_and_push(file, commit_message)

                for file in modified_files:
                    commit_message = f"Updated {os.path.basename(file)}"
                    add_and_push(file, commit_message)

                files.update(current_files)
                change_event.set()  # Signal changes detected

            time.sleep(1)

    threading.Thread(target=file_monitor, daemon=True).start()

    lock = threading.Lock()  # Lock to synchronize add_and_push and delete_and_push functions

    def add_and_push(file, commit_message):
        with lock:
            with open(os.devnull, "w") as devnull:
                subprocess.run(["git", "add", file], stdout=devnull, stderr=devnull)
                subprocess.run(["git", "commit", "-m", commit_message], stdout=devnull, stderr=devnull)
                result = subprocess.run(["git", "push"], capture_output=True, text=True)

                print(f"{YELLOW}Successfully pushed {WHITE}{file}{WHITE}")

                if result.returncode != 0:
                    print(result.stderr)

    def delete_and_push(file, commit_message):
        with lock:
            if file in deleted_files_set:
                return  # Skip if file is already marked as deleted

            with open(os.devnull, "w") as devnull:
                subprocess.run(["git", "rm", file], stdout=devnull, stderr=devnull)
                subprocess.run(["git", "commit", "-m", commit_message], stdout=devnull, stderr=devnull)
                result = subprocess.run(["git", "push"], capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"{YELLOW}Successfully deleted {RED}{file}{WHITE}")
                    deleted_files_set.add(file)  # Mark file as deleted to avoid repetition
                else:
                    print(result.stderr)

    def hash_file(file):
        # Generate the hash of the file content
        with open(file, "rb") as f:
            content = f.read()
            file_hash = hashlib.md5(content).hexdigest()
        return file_hash

    populate_files()

    while True:
        change_event.wait()  # Wait for changes to be detected

        # Reset the event for the next round of changes
        change_event.clear()

if __name__ == "__main__":
    monitor_directory()

