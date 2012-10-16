#!/usr/bin/env python
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here,"README.md")).read()

setup(  
	name="AgileCLU",
	version="0.3.10",
   install_requires=['poster','progressbar','pydes','jsonrpclib'],
	packages=['AgileCLU'],
	package_data={'': ['LICENSE','README.md']},
	include_package_data=True,
	scripts=['bin/agilels', 'bin/agilefetch', 'bin/agilemkdir', 'bin/agilepost', 'bin/agileprofile', 'bin/agilerm', 'bin/agilels.py', 'bin/agilefetch.py', 'bin/agilemkdir.py', 'bin/agilepost.py', 'bin/agileprofile.py', 'bin/agilerm.py'],

	description="Agile Command Line Utilities",
	long_description=readme,
	author="Wylie Swanson",
	author_email="wylie@pingzero.net",
	url = "http://pypi.python.org/pypi/AgileCLU",
	download_url = "https://github.com/wylieswanson/AgileCLU/raw/master/dist/AgileCLU-0.3.10.tar.gz",

	platforms = ("Any",),
	keywords = ("agile", "storage", "limelight", "cloud", "object" ),

	classifiers = [	'Development Status :: 4 - Beta',
							'License :: OSI Approved :: BSD License',
							'Programming Language :: Python',
							'Intended Audience :: End Users/Desktop',
							'Environment :: Console',
							'Topic :: Utilities',
							]
	)
