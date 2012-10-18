#!/usr/bin/env python

from AgileCLU import AgileCLU
from optparse import OptionParser, OptionGroup
from operator import itemgetter
import sys, os.path, string, urllib

def main(*arg):
	# parse command line and associated helper

	parser = OptionParser( usage= "usage: %prog [options] path", version="%prog (AgileCLU "+AgileCLU.__version__+")")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="be verbose", default=False)
        parser.add_option("-l", "--login", dest="username", help="use alternate profile")
	parser.add_option("-r", "--recursive", action="store_true", help="recursive mkdir")

	(options, args) = parser.parse_args()
	if len(args) != 1: parser.error("Wrong number of arguments. Exiting.")
	path = args[0]

	if options.username: agile = AgileCLU( options.username )
	else: agile = AgileCLU()

	# check that destination path exists
	if (agile.exists(path)):
		if options.verbose: print "File or directory object (%s) already exists. Exiting." % path
		agile.logout()
		sys.exit(1)

	if options.recursive: r = agile.mkdir( path, 1 )
	else: r = agile.mkdir( path )

	if (r):
		if options.verbose: print "Directory (%s) has been created. Exiting." % path
	else:
		if options.verbose: print "Directory (%s) failed to be created. Suggest trying recursive option (-r). Exiting." % path

        agile.logout()


if __name__ == '__main__':
    main()
