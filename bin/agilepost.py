#!/usr/bin/env python

from AgileCLU import AgileCLU
from optparse import OptionParser, OptionGroup
import sys, os.path, urllib, subprocess, time

from poster.encode import multipart_encode, get_body_size
from poster.streaminghttp import register_openers
from urllib2 import Request, urlopen, URLError, HTTPError
import progressbar 

pbar = None
fname = None

def progress_callback(param, current, total):
	global pbar
	if (pbar==None):
		widgets = [ unicode(fname, errors='ignore').encode('utf-8'), ' ', progressbar.FileTransferSpeed(), ' [', progressbar.Bar(), '] ', progressbar.Percentage(), ' ', progressbar.ETA() ]
		pbar = progressbar.ProgressBar(widgets=widgets, maxval=total).start()
	try:
		pbar.update(current)
	except AssertionError, e:
		print e

def main(*arg):

	global fname, pbar
	# parse command line and associated helper

	parser = OptionParser( usage= "usage: %prog [options] object path", version="%prog (AgileCLU "+AgileCLU.__version__+")")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="be verbose", default=False)
        parser.add_option("-l", "--login", dest="username", help="use alternate account configuration")

	group = OptionGroup(parser, "Handling Options")
	group.add_option("-r", "--rename", dest="filename", help="rename destination file")
	group.add_option("-c", "--mimetype", dest="mimetype", help="set MIME content-type")
	group.add_option("-t", "--time", dest="mtime", help="set optional mtime")
	group.add_option("-e", "--egress", dest="egress", help="set egress policy (PARTIAL, COMPLETE or POLICY)")
	group.add_option("-m", "--mkdir", action="store_true", help="create destination path, if it does not exist")
	group.add_option("-p", "--progress", action="store_true", help="show transfer progress bar")
	parser.add_option_group(group)
	
	config = OptionGroup(parser, "Configuration Option")
	config.add_option("--username", dest="username", help="Agile username")
	config.add_option("--password", dest="password", help="Agile password")
	config.add_option("--mapperurl", dest="mapperurl", help="Agile MT URL base")
	config.add_option("--apiurl", dest="apiurl", help="Agile API URL")
	config.add_option("--posturl", dest="posturl", help="Agile POST URL")
	parser.add_option_group(config)

	(options, args) = parser.parse_args()
	if len(args) != 2: parser.error("Wrong number of arguments. Exiting.")
	object = args[0]
	path = args[1]
	
	if (not os.path.isfile(object)):
		print "Local file object (%s) does not exist. Exiting." % localfile
		sys.exit(1)

	if options.username: agile = AgileCLU( options.username )
	else: agile = AgileCLU()

	localpath = os.path.dirname(object)
	localfile = os.path.basename(object)

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
	
	if options.filename: fname = options.filename
	else: fname = localfile

	register_openers()

	# video/mpeg for m2ts
	if options.progress: 
		datagen, headers = multipart_encode( { 
			"uploadFile": open(object, "rb"), 
			"directory": path, 
			"basename": fname, 
			"expose_egress": "COMPLETE"
			}, cb=progress_callback)
	else: 
		datagen, headers = multipart_encode( { 
			"uploadFile": open(object, "rb"), 
			"directory": path, 
			"basename": fname, 
			"expose_egress": "COMPLETE"
			} )

	request = Request(agile.posturl, datagen, headers)
	request.add_header("X-Agile-Authorization", agile.token)

	if options.mimetype: mimetype = options.mimetype
	else: mimetype = 'auto'

	request.add_header("X-Content-Type", mimetype )

	success = False ; attempt = 0
	while not success:
		attempt += 1
		try: 
			result = urlopen(request).read() 
			if options.progress: pbar.finish()
			success = True
		except HTTPError, e: 
			if options.progress: pbar.finish()
			print '[!] HTTP Error: ', e.code
			pbar = None
			success = False
		except URLError, e: 
			if options.progress: pbar.finish()
			print '[!] URL Error: ', e.reason
			pbar = None
			success = False

	
	if options.verbose: print "%s%s" % (agile.mapperurlstr(),urllib.quote(os.path.join(path,fname)))

        agile.logout()

if __name__ == '__main__':
    main()


