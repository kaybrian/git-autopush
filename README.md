# Git Autopush
A python package to automate basic git functions.

### Initial Setup
- Configure username & email
````
git config --global user.name "name"
git config --global user.email "example@email.com"
````

- Configure git to store credential
````
git config --global credential.helper store
````

### Developer Setup
- Clone repo:
````
git clone https://github.com/chyna-gvng/git-autopush.git
````

- CD into repo:
````
cd git-autopush
````

- Install locally
````
pip install .
````

### Usage
In the root of the repo you want to work on (leave it to run in the background):
````
git-autopush
````
To exit, press: `CTRL + C`

### Features
- Perform basic git operations; add, commit & push
- Write dynamic commit messages based on filename & actions.
- Actively monitor creation, deletion and modifaction of files & thereafter push the changes to github.