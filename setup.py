from setuptools import setup
from setuptools import find_packages

#packages = find_packages()

setup(
    name='pyClusterFlow',
    version="1.0.0",
    description='pyClusterFlow',
    long_description='',
    author='Jochen Derwae',
    author_email='jochen.derwae@gmail.com',
    license='...',
    entry_points={
        #       "console_scripts": [
        #           "adhesive = adhesive.mainapp:__main"
        #       ]
    },
    install_requires=[
        "addict",
        "networkx",
        "npyscreen",
        "colorama",
        "termcolor_util",
        "PyYAML",
        "click",
        "schedule",
        "python-dateutil",
        "yamldict",
        "Pebble",
        "paramiko",
        "scp"
    ],
    packages=packages,
    package_data={
        #       '': ['*.txt', '*.rst'],
        #       'adhesive': ['py.typed'],
    })
