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


Installation:Linux
------------------
You do not need to download the source code to install AgileCLU.  You can install this from PyPI with one of the following commands (sudo is usually required):

	easy_install AgileCLU

or,

	pip install AgileCLU

If you don't have PyPI installed and you are running on Ubuntu or Debian, install it first.

	sudo apt-get install python-pip

Installation:Mac OSX
--------------------
Python is already installed by default on modern OS X.

Installation:Windows 32-bit and 64-bit
--------------------------------------
Python must be installed on the machine.  You can download from http://www.python.org/getit/ or, specifically, for Windows 32 and 64-bit:

* Python 2.7.3 Windows Installer (Windows binary - does not include source)
	* http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi

* Python 2.7.3 Windows X86-64 Installer (Windows AMD64 / Intel 64 / X86-64 bainry - does not include source)
	* http://www.python.org/ftp/python/2.7.3/python-2.7.3.amd64.msi

Once Python has been installed, you will want to add setuptools, the mainstream package manager for Python, also known as PyPI.

Next, set the system's PATH variable to include directories that include Python components and packages we'll add later.  To do this:

* Click the bottom left Windows icon
* In the search field, type 'system'
* In the Control Panel section of the search results, select "Edit system environment variables"
* Select "Environment Variables"
* In the "System variables" section, scroll down to Path and click "Edit...", and then append ";\Python27;\Python27\Lib\site-packages;\Python27\Scripts;" to the "Variable Value", then select OK.


* For 32-bit version of Python 
	* Install setuptools using the provided .exe installer.
		* http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe

* For 64-bit versions of Python
	* Download ez_setup.py and run it; it will download the appropriate .egg file and install it for you. (Currently, the provided .exe installer does not support 64-bit versions of Python for Windows, due to a distutils installer compatibility issue.
		* http://peak.telecommunity.com/dist/ez_setup.py
		* Run "ez_setup.py"


easy_install AgileCLU

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
