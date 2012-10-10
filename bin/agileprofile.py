#!/usr/bin/env python

# will revisit this later

import AgileCLU, getpass

def main(*arg):

	print "\nagileprofile (AgileCLU " + AgileCLU.AgileCLU.__version__ + ")\n"
	print "This tool generates Agile Storage profile text to be pasted into AgileCLU profile configuration"
	print "files (eg. /etc/agile/agile.conf is the default).  The information should have been provided to"
	print "you by Limelight Networks, often via a \"welcome letter\".  If you have questions regarding the"
	print "account information, please contact support@llnw.com.\n"

	username = raw_input("Enter Agile username: ")

	password1 = "1"
	password2 = "2"
	while (password1 != password2 ):
		password1 = getpass.getpass("Enter Agile password: ")
		password2 = getpass.getpass("Re-enter Agile password: ")

	egress_protocol = "http"
	egress_hostname = raw_input("Enter your egress hostname: " )
	egress_basepath = raw_input("Enter your egress base path: " )

	ingest_protocol = "https"
	ingest_hostname = raw_input("Enter your ingest hostname: " )

	cipher = AgileCLU.e_pw_hash( password1, username, egress_protocol, egress_hostname, egress_basepath )

	print "\n\n### PASTE THE FOLLOWING IN YOUR PROFILE CONFIGURATION FILE ####"
	print "\n[Identity]"
	print "username = "+ username
	print "password = "+ cipher
	print "\n[Egress]"
	print "protocol = "+ egress_protocol
	print "hostname = "+ egress_hostname
	print "basepath = "+ egress_basepath
	print "\n[Ingest]"
	print "protocol = "+ ingest_protocol
	print "hostname = "+ ingest_hostname
	print "\n[Logging]"
	print "enabled = no"
	print "logfile = /var/log/agileclu.log"
	print "level = info"

if __name__ == '__main__':
	main()
