from setuptools import setup

setup(
    name='git-autopush',
    version='0.0.1',
    author='Chyna',
    author_email='angoyewally@gmail.com',
    description='Automates git functions: add, commit, and push.',
    url='https://github.com/yourusername/autopush',
    packages=['autopush'],
    entry_points={
        'console_scripts': [
            'autopush = autopush.autopush:main',
        ],
    },
    install_requires=[
        'watchdog',
        'GitPython',
    ],
)
