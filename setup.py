from setuptools import setup
from setuptools import find_packages


packages = find_packages()

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
        "networkx==2.3",
        "npyscreen==4.10.5",
        "colorama >=0.4.3",
        "termcolor_util >= 1.2.0, <2.0",
        "PyYAML == 5.1.2",
        "click >= 7.0, <8.0",
        "schedule==0.6.0",
        "python-dateutil==2.8.1",
        "yamldict >= 1.2.0, <2.0",
        "Pebble==4.5.3",
        "paramiko==2.6.0",
        "scp"
    ],
    packages=packages,
    package_data={
 #       '': ['*.txt', '*.rst'],
 #       'adhesive': ['py.typed'],
    })
