#!/usr/bin/env python

from AgileCLU import AgileCLU
from optparse import OptionParser, OptionGroup
from urlparse import urlparse
import sys, os.path, urllib

def main(*arg):
	# parse command line and associated helper

	parser = OptionParser( usage= "usage: %prog [options] url path", version="%prog (AgileCLU "+AgileCLU.__version__+")")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="be verbose", default=False)
        parser.add_option("-l", "--login", dest="username", help="use alternate account configuration")

	group = OptionGroup(parser, "Handling Options")
	group.add_option("-r", "--rename", dest="filename", help="rename destination file")
	group.add_option("-m", "--mkdir", action="store_true", help="create destination path, if it does not exist")
	parser.add_option_group(group)

	(options, args) = parser.parse_args()
	if len(args) != 2: parser.error("Wrong number of arguments. Exiting.")
	url = args[0]
	path = args[1]

	if options.username: agile = AgileCLU( options.username )
	else: agile = AgileCLU()

	# check that destination path exists
	if (not agile.exists(path)):
		if options.mkdir: 
			r = agile.mkdir( path, 1 )
			if (r):
				if options.verbose: print "Destination path (%s) has been created. Continuing..." % path
			else:
				if options.verbose: print "Destination path (%s) failed to be created. Suggest trying --mkdir option. Exiting." % path
				agile.logout()
				sys.exit(2)
		else:
			if options.verbose: print "Destination path (%s) does not exist. Suggest --mkdir option. Exiting." % path
			agile.logout()
			sys.exit(1)
	
	o = urlparse( url )
	if options.filename: fname = options.filename
	else: fname = urllib.unquote( os.path.basename( o.path ) )

	r = agile.fetchFileHTTP( os.path.join(path,fname), url )
	if options.verbose: print "%s%s" % (agile.mapperurlstr(),urllib.quote(os.path.join(path,fname)))

        agile.logout()

if __name__ == '__main__':
    main()
