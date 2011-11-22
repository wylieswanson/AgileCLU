#!/usr/bin/env python
# Filename: AgileCLU.py
# coding: utf-8
#
# Copyright (C) 2010-2011, Wylie Swanson
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License V3, as published by
# the Free Software Foundation.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

from jsonrpc import ServiceProxy
import ConfigParser
import sys, os.path

# import sys, subprocess, os.path, string
# from optparse import OptionParser, OptionGroup
# from urlparse import urlparse


cfg = ConfigParser.ConfigParser() 
true = 1
false = 0
version = '0.1'

class	AgileCLU:

        def     __init__(self, username='agile'):

		# Load configuration variables

		if os.path.exists('/etc/agile/'+username+'.conf'): cfg.read('/etc/agile/'+username+'.conf')
		else:
			print "Alternate login identity (%s) configuration does not exist.  Exiting." % username
			sys.exit(1)

		self.uid = cfg.get("Identity", "username")
		upw = cfg.get("Identity", "password")
		self.apiurl = cfg.get("Ingest", "apiurl")
		self.posturl = cfg.get("Ingest", "posturl")
		self.mapperurl = cfg.get("Egress", "mapperurl")
		self.cacheurl = cfg.get("Egress", "mapperurl")

		# connect to API, authenticate, and get a token

		self.api = ServiceProxy( self.apiurl )
		self.token, self.user = self.api.login( self.uid, upw )
	
	def	apiurlstr(self):
		return self.apiurl

	def	posturlstr(self):
		return self.posturl

	def	mapperurlstr(self):
		return self.mapperurl

	def	cacheurlstr(Self):
		return self.cacheurl

	def	stat(self, path):
		r = self.api.stat( self.token, path )
		return r

	def	logout(self):
		r = self.api.logout( self.token )
		return r

	def	noop(self):
		r = self.api.noop( self.token )
		return r

	def	listDir(self, path, pageSize=10000, cookie=1, stat=True ):
		r = self.api.listDir( self.token, path, pageSize, cookie, stat )
		return r

	def	listFile(self, path, pageSize=10000, cookie=1, stat=True ):
		r = self.api.listFile( self.token, path, pageSize, cookie, stat )
		return r

	def	makeDir(self, path):
		r = self.api.makeDir( self.token, path)
		return r

	def	makeDir2(self, path):
		r = self.api.makeDir2( self.token, path)
		return r

	def	deleteFile(self, path):
		r = self.api.deleteFile( self.token, path)
		return r

	def	rm(self, path):
		if (self.fexists(path)):
			r = self.deleteFile(path)
			if (r == 0): return true
			else: return false

	def	deleteDir(self, path):
		r = self.api.deleteDir( self.token, path)
		return r

	def	deleteObject(self, path):
		r = self.api.deleteObject( self.token, path)
		return r

	def	rename(self, path, newpath):
		r = self.api.rename( self.token, path, newpath)
		return r
	
	def	copyFile(self, path, newpath):
		r = self.api.copyFile( self.token, path, newpath)
		return r

	def	registerCallback( self, uri, flags=0, threshold=0 ):
		r = self.api.registerCallback( self.token, uri, flags, threshold )
		return r

	def	listCallback( self ):
		r = self.api.listCallback( self.token )
		return r

	def	fetchFileHTTP( self, path, uri, username=None, password=None, auth=None, callbackid=0, priority=0, flags=0, expose_egress='POLICY'):
		r = self.api.fetchFileHTTP( self.token, path, uri, username, password, auth, callbackid, priority, flags, expose_egress)
		return r

	def	fetchFileFTP(self, path, hostname, filename, username=None, password=None, port=21, passive=True, callbackid=0, priority=0, flags=0, expose_egress='POLICY'):
		r = self.api.fetchFileFTP( self.token, path, hostname, filename, username, password, port, passive, callbackid, priority, flags, expose_egress)
		return r

	def	fexists( self, path ):
		r = self.stat( path )
		if ((r['code'] == 0) and (r['type'] == 2)): return true
		else: return false

	def	dexists( self, path ):
		r = self.stat( path )
		if ((r['code'] == 0) and (r['type'] == 1)): return true
		else: return false

	def	exists(self, path):
		if (self.fexists(path) or self.dexists(path)): return true
		else: return false

	def	mkdir(self, path, recursive = False):
		if (not self.dexists(path)):
			if (recursive):
				r = self.makeDir2( path )
			else:
				r = self.makeDir( path )
			if (r == 0): return true
			else: return false
		else:	
			return false

# End of agile.py
