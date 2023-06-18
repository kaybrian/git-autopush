from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="git-autopush",
    version="0.0.2",
    author="Chyna",
    author_email="angoyewally@gmail.com",
    description="Automates git functions: git add, git commit, and git push",
    license="MIT",
    url="https://github.com/chyna-gvng/git-autopush",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        # List your dependencies here, if any
    ],
)
