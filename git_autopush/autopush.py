import os
import time
import subprocess

def monitor_directory():
    path = os.getcwd()  # Get the current working directory
    if not os.path.exists(os.path.join(path, ".git")):
        print("Directory is not a git repo!")
        return

    files = {}

    while True:
        current_files = {filename: os.stat(filename).st_mtime for filename in os.listdir(path)}

        added_files = current_files.keys() - files.keys()
        deleted_files = files.keys() - current_files.keys()
        modified_files = {
            filename for filename in files.keys() & current_files.keys()
            if files[filename] != current_files[filename]
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

        files = current_files
        time.sleep(1)  # Sleep for 1 second before checking again

def add_and_push(file, commit_message):
    subprocess.run(["git", "add", file])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    monitor_directory()
