# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from pyslash import __version__


setup(
    name='pyslash',
    version=__version__,
    description='Tools for parsing nikkansports.com',
    author='Jun-ya HASEBA',
    author_email='7pairs@gmail.com',
    url='http://seven-pairs.hatenablog.jp/',
    packages=find_packages(exclude=['tests']),
    install_requires=['beautifulsoup4', 'docopt'],
    entry_points="""\
    [console_scripts]
    pyslash = pyslash.executor:main
    """
)
