#!/usr/bin/env python
from glob import glob
from setuptools import setup, find_packages
import sys

setup(  
	name="AgileCLU",
	version="0.3.0",
   install_requires=['poster','progressbar','pydes','jsonrpclib'],

	description="Agile Command Line Utilities",
	long_description="""
This package uses the Limelight Networks Agile Storage APIs to manage objects in the Agile Cloud.
""",

	author="Wylie Swanson",
	author_email="wylie@pingzero.net",
	url="http://www.pingzero.net",
	download_url = "http://www.pingzero.net/downloads/AgileCLU-0.3.0.tar.gz",

	classifiers = [	'Development Status :: 4 - Beta',
							'License :: OSI Approved :: BSD License',
							'Programming Language :: Python',
							'Intended Audience :: End Users/Desktop',
							'Environment :: Console',
							'Topic :: Utilities',
							],

	platforms = ("Any",),
	keywords = ("agile", "storage", "limelight", "cloud", "object" ),

	packages=['AgileCLU'],
	scripts=glob("bin/*"),
	data_files=[
		( '/etc/agile/', glob('agile/*') ),
	]
	)
