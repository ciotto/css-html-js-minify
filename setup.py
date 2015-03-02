#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Setup.py for Python Wheels, as Generic as possible."""


import os

from setuptools import setup


MODULE_RELATIVE_PATH = os.path.join(os.getcwd(), "css-html-js-minify.py")


def find_this(search, filename=MODULE_RELATIVE_PATH):
    """Take a REGEX and a filename path string and return the found value."""
    if not search:
        return
    for line in open(str(filename)).readlines():
        if search in line:
            line = line.split("=")[1].strip()
            if search in "__version__":
                return line.replace("'", "").replace('"', '')
            return line


setup(

    name="css-html-js-minify",
    version=find_this("__version__"),

    description=find_this("__description__"),
    long_description=(open('README.rst').read().strip()),

    url=find_this("__url__"),
    license=find_this("__licence__"),

    author=find_this("__author__"),
    author_email=find_this("__email__"),
    maintainer=find_this("__author__"),
    maintainer_email=find_this("__email__"),

    include_package_data=True,
    zip_safe=True,

    scripts=["css-html-js-minify.py"],
    entry_points = {
        'console_scripts': ['css-html-js-minify = css_html_js_minify']
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',

        'Natural Language :: English',

        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',

        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
