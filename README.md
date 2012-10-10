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

or,

	pip install AgileCLU

If you don't have PyPI installed and you are running on Ubuntu or Debian, install it first.

	sudo apt-get install python-pip

Upgrading
---------
If you are upgrading from a release prior to 0.3.1, you may need to manually delete the files from your Python installation (egg and easy-install.pth) prior to invoking easy_install or pip.  For future upgrades, can force to latest version with:

	easy_install -U AgileCLU


Configuration 
-------------
After installing AgileCLU, run use the profile tool to generate the proper output to place in an /etc/agile/agile.conf configuration file.  You can create as many configuration profiles as you like, specifying to use them over the default agile.conf profile by specifying the -l option on any given command.

	agileprofile

Example output:

	agileprofile (AgileCLU 0.3.6)
	
	This tool generates Agile Storage profile text to be pasted into AgileCLU profile configuration
	files (eg. /etc/agile/agile.conf is the default).  The information should have been provided to
	you by Limelight Networks, often via a "welcome letter".  If you have questions regarding the
	account information, please contact support@llnw.com.
	
	Enter Agile username: testcompany
	Enter Agile password: 
	Re-enter Agile password: 
	Enter your egress hostname: global.mt.lldns.net
	Enter your egress base path: /testcompany
	Enter your ingest hostname: api.agile.lldns.net
	
	PASTE THE FOLLOWING IN YOUR PROFILE CONFIGURATION FILE 
	
	[Identity]
	username = testcompany
	password = A4UsWnRpKOdNy0HNWDHY+Q==
	
	[Egress]
	protocol = http
	hostname = global.mt.lldns.net
	basepath = /testcompany
	
	[Ingest]
	protocol = https
	hostname = api.agile.lldns.net
	
	[Logging]
	enabled = no
	logfile = /var/log/agileclu.log
	level = info

Requirements
------------
This package has the following requirements:

* An account on Limelight Network's Agile Storage cloud platform. (http://www.limelightnetworks.com)
* poster by Chris AtLee - used for streaming ingest (http://atlee.ca/software/poster/)
* progressbar by Nilton Volpato - used for console ingest progress bar (http://code.google.com/p/python-progressbar/)
* pydes by Todd Whiteman - used as part of the password encryption scheme for config files (http://twhiteman.netfirms.com/des.html)
* jsonrpclib by John Marshall - an implementation of the JSON-RPC specification (https://github.com/joshmarshall/jsonrpclib)

Storage Locations
-----------------
As of October 2012, the Agile Storage Cloud has storage capacity in 34 geographies around the world.

![Agile Storage Locations](https://raw.github.com/wylieswanson/AgileCLU/master/agile_locations_oct_2012.jpg)
