<<<<<<< HEAD
from setuptools import setup
from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

packages = find_packages()

extras_require = {
    'ssh': ['paramiko==2.6.0']
}

setup(
    name='adhesive',
    version="1.5.0",
    description='adhesive',
    long_description=readme,
    author='Bogdan Mustiata',
    author_email='bogdan.mustiata@gmail.com',
    license='BSD',
    entry_points={
        "console_scripts": [
            "adhesive = adhesive.mainapp:__main"
        ]
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
    ],
    extras_require=extras_require,
    packages=packages,
    package_data={
        '': ['*.txt', '*.rst'],
        'adhesive': ['py.typed'],
    })
=======
#!/usr/bin/env python
# encoding: utf-8
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.dirname(__file__)
exec(open(os.path.join(here, 'rpyc', 'version.py')).read())

setup(name="rpyc",
      version=version_string,  # @UndefinedVariable
      description="Remote Python Call (RPyC), a transparent and symmetric RPC library",
      author="Tomer Filiba",
      author_email="tomerfiliba@gmail.com",
      maintainer="James Stronz",
      maintainer_email="james@network-perception.com",
      license="MIT",
      url="http://rpyc.readthedocs.org",
      packages=[
          'rpyc',
          'rpyc.core',
          'rpyc.lib',
          'rpyc.utils',
      ],
      scripts=[
          os.path.join("bin", "rpyc_classic.py"),
          os.path.join("bin", "rpyc_registry.py"),
      ],
      tests_require=[],
      test_suite='nose.collector',
      install_requires=["plumbum"],
      #    entry_points = dict(
      #        console_scripts = [
      #            "rpyc_classic = rpyc.scripts.rpyc_classic:main",
      #            "rpyc_registry = rpyc.scretips.rpyc_registry:main",
      #        ],
      #    ),
      platforms=["POSIX", "Windows"],
      python_requires='>=3.6',
      use_2to3=False,
      zip_safe=False,
      long_description=open(os.path.join(here, "README.rst"), "r").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Topic :: Internet",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Software Development :: Object Brokering",
          "Topic :: Software Development :: Testing",
          "Topic :: System :: Clustering",
          "Topic :: System :: Distributed Computing",
          "Topic :: System :: Monitoring",
          "Topic :: System :: Networking",
          "Topic :: System :: Systems Administration",
      ],
      )
>>>>>>> rpyc/master
