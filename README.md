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

Summary
-------

Requirements
------------
This package has the following requirements:

* An account on Limelight Network's Agile Storage cloud platform. (http://www.limelightnetworks.com)
* poster by Chris AtLee - used for streaming ingest (http://atlee.ca/software/poster/)
* progressbar by Nilton Volpato - used for console ingest progress bar (http://code.google.com/p/python-progressbar/)
* pydes by Todd Whiteman - used as part of the password encryption scheme for config files (http://twhiteman.netfirms.com/des.html)
* jsonrpclib by John Marshall - an implementation of the JSON-RPC specification (https://github.com/joshmarshall/jsonrpclib)

Installation
------------
You can install this from PyPI with one of the following commands (sudo is usually required):

	easy_install AgileCLU
	pip install AgileCLU

Configuration 
-------------
After installing AgileCLU, run "agileprofile" and put the output in /etc/agile/agile.conf.
