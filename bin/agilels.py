#!/usr/bin/env python

from AgileCLU import AgileCLU
from optparse import OptionParser, OptionGroup
from operator import itemgetter
import sys, os.path, string, urllib

def sizeof_fmt(num):
        for x in ['bytes','KB','MB','GB','TB']:
                if num < 1024.0: return "%3.1f %s" % (num, x)
                num /= 1024.0

def main(*arg):

	# parse command line and associated helper

	parser = OptionParser( usage= "usage: %prog [options] path", version="%prog (AgileCLU "+AgileCLU.__version__+")")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="be verbose", default=False)
        parser.add_option("-l", "--login", dest="username", help="use alternate profile")
	parser.add_option("-r", "--recurse", action="store_true", help="recurse directories")

	group = OptionGroup(parser, "Output options")
	group.add_option("-b", "--bytes", action="store_true", help="include file size bytes")
	group.add_option("-s", "--sizes", action="store_true", help="report things like bytes in human-readable format")
	group.add_option("-u", "--url", action="store_true", help="include egress URLs")
	group.add_option("-f", "--filehide", action="store_true", help="hide file objects")
	group.add_option("-d", "--dirhide", action="store_true", help="hide directory objects")
	parser.add_option_group(group)

	""" Placeholder for using command line for profile information 
	profile = OptionGroup(parser, "Profile options")
	profile.add_option("--username", dest="username", help="Agile username")
	profile.add_option("--password", dest="password", help="Agile password")
	profile.add_option("--iprotocol", dest="ingest_protocol", help="Agile ingest protocol", default="https")
	profile.add_option("--ihostname", dest="ingest_hostname", help="Agile ingest hostname", default="api.agile.lldns.net")
	profile.add_option("--eprotocol", dest="egress_protocol", help="Agile egress protocol", default="http")
	profile.add_option("--ehostname", dest="egress_hostname", help="Agile egress hostname", default="global.mt.lldns.net")
	profile.add_option("--ebase", dest="egress_basepath", help="Agile egress base path" )
	parser.add_option_group(profile)
	"""

	(options, args) = parser.parse_args()
	if len(args) != 1 and len(args) != 0: parser.error("Wrong number of arguments. Exiting.")
	if len(args) == 0: 
		path = '/'
	else: 
		path = args[0]

	if options.username: agile = AgileCLU( options.username )
	else: agile = AgileCLU()

	# check that destination path exists
	if (not agile.exists(path)):
		if options.verbose: print "File or directory object (%s) does not exist. Exiting." % path
		agile.logout()
		sys.exit(1)

        else:

		class DirWalker(object):

			def walk(self,path,meth):
				dir = agile.listDir( path,  1000, 0, 1 )
				dir['list'] = sorted(dir['list'], key=str)
                		for item in dir['list']:
		                        itemurl = os.path.join(path,item['name'])
					if not options.dirhide: print "["+itemurl+"]"
					if not options.filehide: meth(itemurl)
		                        self.walk(itemurl,meth)

		def FileWalker(object):
                	fl = agile.listFile(object, 1000, 0, 1)
			items = fl['list']
			items = sorted( items, key=itemgetter('name'))
			items = sorted( items, key=lambda x: x['name'].lower())
	                for item in items:
	                        if options.url: 
					itemurl = "%s%s" % (agile.mapperurlstr(),  urllib.quote(os.path.join( object, item['name'] )))
	                        else: 
					itemurl = os.path.join(object,item['name'])
	                        if options.bytes: 
	                                if options.sizes: itemurl += " "+sizeof_fmt(item['stat']['size'])
	                                else: itemurl += " "+str(item['stat']['size'])+" bytes"
	                        print itemurl

		if options.recurse: 
			DirWalker().walk(path,FileWalker)
		else: 
                        dir = agile.listDir( path,  1000, 0, 1 )
			dir['list'] = sorted(dir['list'], key=str)
                        for item in dir['list']:
                        	itemurl = os.path.join(path,item['name'])
				if not options.dirhide: print "["+itemurl+"]"
			FileWalker(path)

        agile.logout()


if __name__ == '__main__':
    main()
