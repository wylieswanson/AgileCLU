#!/usr/bin/env python

import AgileCLU, ConfigParser, sys, os, getpass
from optparse import OptionParser, OptionGroup

config_path = os.path.expanduser( '~/.agileclu/' )
default_config = os.path.join( config_path, 'default.conf' )

config = ConfigParser.SafeConfigParser()

def	delete_profile( profile ):
	if not os.path.isfile( os.path.join( config_path, profile+'.conf' ) ):
		print "The (%s) profile does not exist.  Exiting." % ( profile ) 
	else:
		try: 
			os.unlink( os.path.join( config_path, profile+'.conf' ) )
		except:
			print "Failed to remove (%s) profile.  Exiting." % (profile)
		else:
			print "The (%s) profile has been removed.  Exiting." % (profile)

def	view_profile( profile ):
	if not os.path.isfile( os.path.join( config_path, profile+'.conf' ) ):
		print "The (%s) profile does not exist.  Exiting." % ( profile ) 
	else:
		with open ( os.path.join( config_path, profile+'.conf' ), 'r' ) as f:
			read_data = f.read()
		print read_data

def	prompt( str, default, command, password=False ):
	width=50
	#if command=='modify':
	if default<>'' and not password:
		str += ' [%s]' % default
	
	if password:
		str += ' '
		value = getpass.getpass(' '+str.rjust(width)+': ')
	else:
		print str.rjust(width),
		value = raw_input(': ')
	if value=='': value=default
	return value


def	edit_profile( profile, command ):
	width = 50

	if command=='create':
		if os.path.isfile( os.path.join( config_path, profile+'.conf' ) ):
			print "Profile (%s) already exists.  You must use delete first, or use modify.  Exiting." % (profile)
			sys.exit(1)
		username='' ; password='' 
		egress_protocol='http' ; egress_hostname='global.mt.lldns.net' ; egress_basepath='' ; 
		ingest_protocol='https' ; ingest_hostname='' 

	elif command=='modify':
		config.read( os.path.join( config_path, profile+'.conf' ) ) 

		username=config.get( "Identity", "username" )
		password=config.get( "Identity", "password" )
		egress_protocol=config.get( "Egress", "protocol" )
		egress_hostname=config.get( "Egress", "hostname" )
		egress_basepath=config.get( "Egress", "basepath" )
		ingest_protocol=config.get( "Ingest", "protocol" )
		ingest_hostname=config.get( "Ingest", "hostname" )

	ciphered = 0
	print command.upper()+ " PROFILE: "+profile
	try:
		username = prompt( 'Username', username, command )

		if command=='modify':
			password2 = password
			password = prompt( 'Password', password, command, True )
			if ( password != password2 ):
				while (password != password2 ):
					password = prompt( 'Password', '', command, True )
					password2 = prompt( "Re-enter password", '', command, True )
			else: ciphered=1
		else:
			password = "1" ; password2 = "2"
			while (password != password2 ):
				password = prompt( 'Password', password, command, True )
				password2 = prompt( "Re-enter password", password2, command, True )

		egress_protocol = prompt( 'Egress protocol', egress_protocol, command )
		egress_hostname = prompt( 'Egress hostname', egress_hostname, command )
		egress_basepath = prompt( "Egress base path", egress_basepath, command )

		ingest_protocol = prompt( 'Ingest protocol', ingest_protocol, command )
		ingest_hostname = prompt( 'Ingest hostname', ingest_hostname, command )

		if not ciphered:
			cipher = AgileCLU.e_pw_hash( password, username, egress_protocol, egress_hostname, egress_basepath )
		else:	
			cipher = password

	except (KeyboardInterrupt, SystemExit):
		print "\nAborting..."
		sys.exit(1)
	
	if command=='modify':
		try:
			os.unlink( os.path.join( config_path, profile+'.conf' ) )
		except:
			print "Failed to remove (%s) profile.  Exiting." % (profile)
			sys.exit(1)
		config.remove_section('AgileCLU')
		config.remove_section('Identity')
		config.remove_section('Egress')
		config.remove_section('Ingest')
		config.remove_section('Logging')



	config.add_section("AgileCLU")
	config.set("AgileCLU", "version", AgileCLU.AgileCLU.__version__ )

	config.add_section("Identity")
	config.set("Identity", "username", username )
	config.set("Identity", "password", cipher )

	config.add_section("Egress")
	config.set("Egress", "protocol", egress_protocol )
	config.set("Egress", "hostname", egress_hostname )
	config.set("Egress", "basepath", egress_basepath )

	config.add_section("Ingest")
	config.set("Ingest", "protocol", ingest_protocol )
	config.set("Ingest", "hostname", ingest_hostname )
	
	config.add_section("Logging")
	config.set("Logging", "enabled", "no" )
	config.set("Logging", "logfile", "/var/log/agileclu.log" )
	config.set("Logging", "level", "info" )


	config.write( open( os.path.join( config_path, profile+'.conf' ) , "w"))
	print "\nProfile (%s) has been" % (profile),
	if command=='modify':
		print "updated.",
	else:
		print "saved.",
	print " Exiting.\n" 

def	list_profile():

	print "List Profiles\n-------------"
	profiles = os.listdir( os.path.expanduser(config_path) )
	if len(profiles)==0:
		print "You do not have any profiles.  Use \"create\" to make one.\n"
	for profile in profiles:
		print profile.replace('.conf','')

def	main(*arg):

	parser = OptionParser( 
		usage= "usage: %prog create|delete|modify|list [profile]",
		version="%prog (AgileCLU "+AgileCLU.AgileCLU.__version__+")")

	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="be verbose", default=False)

	(options, args) = parser.parse_args()
	if len(args) < 1 or len(args) > 2: parser.error("Wrong number of arguments. Use -h for more information.")

	command = args[0].lower()
	if len(args)==2: 
		profile = args[1].lower()
	else:
		profile = 'default'

	if not os.path.isdir( config_path):
		try: 
			os.mkdir( config_path, 0700 )
		except OSError:
			print "Failed to create profile directory (%s).  Please check permissions." % (config_path)

	print "\n" + os.path.basename(__file__) + " (AgileCLU "+AgileCLU.AgileCLU.__version__+")\n"

	if not command in ['create','delete','modify','list', 'view' ]:
		parser.error("You must use create, delete, modify or list. Exiting.")

	if command=='list': list_profile()
	if command=='view': view_profile( profile )
	if command=='create': edit_profile( profile, command )
	if command=='modify': edit_profile( profile, command )
	if command=='delete': delete_profile( profile )

if __name__ == '__main__':
	main()
