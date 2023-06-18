import os
import time
import subprocess
import signal
import sys
import hashlib
import threading

def monitor_directory(path="."):
    if not os.path.exists(os.path.join(path, ".git")):
        print("Directory is not a Git repo!")
        return

    print("Monitoring...")

    files = {}

    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            files[full_path] = hash_file(full_path)

    def exit_gracefully(signal, frame):
        print("\nGoodbye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_gracefully)

    change_event = threading.Event()  # Event object to signal changes
    processed_change = False  # Flag to indicate if a change has been processed

    def file_monitor():
        nonlocal processed_change
        while True:
            current_files = {filename: hash_file(filename) for filename in files.keys()}

            if current_files != files:  # Check for changes
                added_files = current_files.keys() - files.keys()
                deleted_files = files.keys() - current_files.keys()
                modified_files = {
                    filename for filename in files.keys() & current_files.keys()
                    if files[filename] != current_files[filename]
                }

                for file in added_files:
                    commit_message = f"Created {os.path.basename(file)}"
                    add_and_push(file, commit_message)
                    processed_change = True

                for file in deleted_files:
                    commit_message = f"Deleted {os.path.basename(file)}"
                    add_and_push(file, commit_message)
                    processed_change = True

                for file in modified_files:
                    commit_message = f"Updated {os.path.basename(file)}"
                    add_and_push(file, commit_message)
                    processed_change = True

                files.update(current_files)

                if processed_change:
                    change_event.set()  # Signal changes detected
                    processed_change = False

            time.sleep(1)

    threading.Thread(target=file_monitor, daemon=True).start()

    while True:
        change_event.wait()  # Wait for changes to be detected

        # Reset the event for the next round of changes
        change_event.clear()

        # Sleep indefinitely until changes are detected again
        change_event.wait()

def hash_file(file):
    # Generate the hash of the file content
    with open(file, "rb") as f:
        content = f.read()
        file_hash = hashlib.md5(content).hexdigest()
    return file_hash

def add_and_push(file, commit_message):
    subprocess.run(["git", "add", file])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    monitor_directory()

