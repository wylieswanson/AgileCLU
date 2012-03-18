#!/usr/bin/env python
from glob import glob
from distutils.core import setup

setup(  name="AgileCLU",
	version="0.1",
	description="Limelight Networks Agile Cloud Storage - API Command Line Utilities",
	author="Wylie Swanson",
	author_email="wylie@pingzero.net",
	url="http://www.pingzero.net",
	package_dir={'': 'src'},
	packages=[''],
	scripts=glob("bin/*"),
	data_files=[
		( '/etc/agile/', glob('agile/*') ),
	]
	)


