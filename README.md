AgileCLU
========
This library and script package is an implementation of command line tools and Python module 
that can be used to write software against Limelight Networks' Agile Storage cloud platform.
It leverages Agile Storage's JSON-RPC APIs to manage, ingest and egress objects from the 
Agile Cloud.

Communication
-------------
Feel free to send any questions, comments, or patches to my Github page (you'll need to join 
to send a message): 
https://github.com/wylieswanson/AgileCLU


Installation
------------
You do not need to download the source code to install AgileCLU.  You can install this from PyPI with one of the following commands (sudo is usually required):

	easy_install AgileCLU
	pip install AgileCLU

If you don't have PyPI installed and you are running on Ubuntu or Debian, install it first.

	sudo apt-get install python-pip

Configuration 
-------------
After installing AgileCLU, run use the profile tool to generate the proper output to place in an /etc/agile/agile.conf configuration file.  You can create as many configuration profiles as you like, specifying to use them over the default agile.conf profile by specifying the -l option on any given command.

	agileprofile

Requirements
------------
This package has the following requirements:

* An account on Limelight Network's Agile Storage cloud platform. (http://www.limelightnetworks.com)
* poster by Chris AtLee - used for streaming ingest (http://atlee.ca/software/poster/)
* progressbar by Nilton Volpato - used for console ingest progress bar (http://code.google.com/p/python-progressbar/)
* pydes by Todd Whiteman - used as part of the password encryption scheme for config files (http://twhiteman.netfirms.com/des.html)
* jsonrpclib by John Marshall - an implementation of the JSON-RPC specification (https://github.com/joshmarshall/jsonrpclib)

