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
In the root of the repo you want to work on:
````
git-autopush
````