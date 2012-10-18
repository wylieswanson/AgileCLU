#!/usr/bin/env python

from AgileCLU import AgileCLU
from optparse import OptionParser, OptionGroup
import sys, os.path, string, urllib

def main(*arg):

	# parse command line and associated helper

	parser = OptionParser( usage= "usage: %prog [options] path", version="%prog (AgileCLU "+AgileCLU.__version__+")")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="be verbose", default=False)
	parser.add_option("-l", "--login", dest="username", help="use alternate profile")

	(options, args) = parser.parse_args()
	if len(args) != 1: parser.error("Wrong number of arguments. Exiting.")
	path = args[0]

	if options.username: agile = AgileCLU( options.username )
	else: agile = AgileCLU()

	# check that destination path exists
	if not agile.exists(path):
		if options.verbose: print "Directory (%s) does not exist. Exiting." % path
		agile.logout()
		sys.exit(1)

	if not agile.dexists(path):
		if options.verbose: print "Directory (%s) is a file?  Exiting." % path
		agile.logout()
		sys.exit(2)

	result = agile.deleteObject(path)
	if result:
		print result
		if options.verbose: print "Directory (%s) was recursively removed." % path
	else:
		if options.verbose: print "Directory (%s) was not successfully removed.  Exiting." % path
		agile.logout()
		sys.exit(3)

        agile.logout()

if __name__ == '__main__':
    main()
