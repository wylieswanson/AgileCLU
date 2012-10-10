import jsonrpclib
import ConfigParser, sys, os.path, logging
import poster 
import pyDes, md5, hashlib, base64
from urllib2 import Request, urlopen, URLError, HTTPError


logger = logging.getLogger('AgileCLU')
logger.addHandler(logging.NullHandler())
cfg = ConfigParser.ConfigParser() 

def epwbasekey( username, proto, hostname, basepath ):
   m = md5.new()
   m.update( username )
   m.update( proto )
   m.update( hostname )
   m.update( basepath )
   key = base64.b64encode(hashlib.sha256( m.digest() ).digest())
   return key[0:24]

def e_pw_hash( str, username, proto, hostname, basepath ):
   return base64.b64encode(pyDes.triple_des(epwbasekey(username,proto,hostname,basepath)).encrypt(str, padmode=2))

def e_pw_dehash( str, username, proto, hostname, basepath ):
	basekey=epwbasekey(username,proto,hostname,basepath)
	try:
		b64decode=base64.b64decode(str)
	except TypeError, ValueError:
		b64decode="12345678"
	try:
		if (len(b64decode) % 8 == 0):
			dehash = pyDes.triple_des(basekey).decrypt(b64decode, padmode=2)
		else:
			print "Password is not valid. Verify profile was built with \"agileprofile\" command."
			sys.exit(1)
	except TypeError, ValueError:
		dehash = "87654321"
	if dehash is '': dehash='87654321' 
	return dehash

class	AgileCLU:
	__module__ = "AgileCLU"
	__version__ = "0.3.6"

	def     __init__(self, profile='agile'):

		# Load configuration variables

		if os.path.exists('/etc/agile/'+profile+'.conf'): cfg.read('/etc/agile/'+profile+'.conf')
		else:
			print "Profile (%s) does not exist.  Create profile with \"agileprofile\" command." % profile
			# logger.critical( "configuration /etc/agile/"+profile+".conf does not exist" )
			sys.exit(1)

		# minor check to look for compliant configuration file
		if not cfg.has_option("Egress","protocol"):
			print "Profile (%s) is not valid!  Create profile with \"agileprofile\" command." % profile
			sys.exit(1)


		self.uid = cfg.get("Identity", "username")

		self.egress_protocol = cfg.get("Egress", "protocol")
		self.egress_hostname = cfg.get("Egress", "hostname")
		self.egress_basepath = cfg.get("Egress", "basepath")
		
		self.ingest_protocol = cfg.get("Ingest", "protocol")
		self.ingest_hostname = cfg.get("Ingest", "hostname")

		self.mapperurl = self.egress_protocol + "://" + self.egress_hostname + self.egress_basepath
	
		self.apiurl = self.ingest_protocol + "://" + self.ingest_hostname + "/jsonrpc"
		self.posturl = self.ingest_protocol + "://" + self.ingest_hostname + "/post/file"

		upw = e_pw_dehash( 
			cfg.get("Identity", "password"), 
			self.uid, 
			self.egress_protocol, 
			self.egress_hostname, 
			self.egress_basepath )

		if upw is "87654321":
			print "Password is not valid!  Verify profile was built with \"agileprofile\" command."
			sys.exit(1)

		# initialize the logger for session
		if cfg.getboolean("Logging", "enabled" ):
			hdlr = logging.FileHandler( '/var/log/agileclu.log' )
			formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
			hdlr.setFormatter(formatter)
			logger.addHandler(hdlr)
			logger.setLevel(logging.INFO)

		# connect to API, authenticate, and get a token
		self.api = jsonrpclib.Server( self.apiurl )
		self.token, self.user = self.api.login( self.uid, upw )
		if self.token is None:
			print "Authentication for '"+str(self.uid)+"' failed!  It is recommended to generate a new profile with \"agileprofile\" command."
			logger.critical( self.uid+" login failed - check account credentials" )
			sys.exit(1)

		logger.info( self.uid+" "+self.token+", login "+str(self.user)+" tokenized" )
	
	def	apiurlstr(self):
		logger.info( self.uid+" "+self.token+", apiurl="+self.apiurl )
		return self.apiurl

	def	posturlstr(self):
		logger.info( self.uid+" "+self.token+", posturl="+self.posturl )
		return self.posturl

	def	mapperurlstr(self):
		logger.info( self.uid+" "+self.token+", mapperurl="+self.mapperurl )
		return self.mapperurl

	def	cacheurlstr(self):
		logger.info( self.uid+" "+self.token+", cacheurl="+self.cacheurl )
		return self.cacheurl

	def	tokenstr(self):
		logger.info( self.uid+" "+self.token+", self.token" )
		return self.token

	def	stat(self, path):
		r = self.api.stat( self.token, path )
		logger.info( self.uid+" "+self.token+", stat "+path+" = "+str(r) )
		return r

	def	logout(self):
		r = self.api.logout( self.token )
		logger.info( self.uid+" "+self.token+", logout = "+str(r)+", detokenized" )
		return r

	def	noop(self):
		r = self.api.noop( self.token )
		logger.info( self.uid+" "+self.token+", noop = "+str(r) )
		return r

	def	listDir(self, path, pageSize=10000, cookie=0, stat=True ):
		r = self.api.listDir( self.token, path, pageSize, cookie, stat )
		logger.info( self.uid+" "+self.token+", listDir "+path+" pageSize "+str(pageSize)+" cookie "+str(cookie)+" stat "+str(stat) )
		# +" = "+str(r) )
		return r

	def	listFile(self, path, pageSize=10000, cookie=0, stat=True ):
		r = self.api.listFile( self.token, path, pageSize, cookie, stat )
		logger.info( self.uid+" "+self.token+", listFile "+path+" pageSize "+str(pageSize)+" cookie "+str(cookie)+" stat "+str(stat) )
		# +" = "+str(r) )
		return r

	def	makeDir(self, path):
		r = self.api.makeDir( self.token, path)
		logger.info( self.uid+" "+self.token+", makeDir "+path+" = "+str(r) )
		return r

	def	makeDir2(self, path):
		r = self.api.makeDir2( self.token, path)
		logger.info( self.uid+" "+self.token+", makeDir2 "+path+" = "+str(r) )
		return r

	def	deleteFile(self, path):
		r = self.api.deleteFile( self.token, path)
		logger.info( self.uid+" "+self.token+", deleteFile "+path+" = "+str(r) )
		return r

	def	rm(self, path):
		if (self.fexists(path)):
			r = self.deleteFile(path)
			if (r == 0): 
				logger.info( self.uid+" "+self.token+", rm "+path+" succeeded" )
				return True
			else: 
				logger.warning( self.uid+" "+self.token+", rm "+path+" failed" )
				return False
		else:
			logger.warning( self.uid+" "+self.token+", rm "+path+" skipped nonexistent file" )

	def	deleteDir(self, path):
		r = self.api.deleteDir( self.token, path)
		logger.info( self.uid+" "+self.token+", deleteDir "+path+" = " + str(r) )
		return r

	def	deleteObject(self, path):
		r = self.api.deleteObject( self.token, path)
		logger.info( self.uid+" "+self.token+", deleteObject "+path+" = " + str(r) )
		return r

	def	rename(self, path, newpath):
		r = self.api.rename( self.token, path, newpath)
		logger.info( self.uid+" "+self.token+", rename "+path+" to "+newpath+" = " + str(r) )
		return r
	
	def	copyFile(self, path, newpath):
		r = self.api.copyFile( self.token, path, newpath)
		logger.info( self.uid+" "+self.token+", copyFile "+path+" to "+newpath+" = " + str(r) )
		return r

	def	registerCallback( self, uri, flags=0, threshold=0 ):
		r = self.api.registerCallback( self.token, uri, flags, threshold )
		logger.info( self.uid+" "+self.token+", registerCallback "+uri+" flags "+str(flags)+" threshold "+str(threshold)+" = " + str(r) )
		return r

	def	listCallback( self ):
		r = self.api.listCallback( self.token )
		logger.info( self.uid+" "+self.token+", listCallback" )
		return r

	def	fetchFileHTTP( self, path, uri, username=None, password=None, auth=None, callbackid=0, priority=0, flags=0, expose_egress='COMPLETE'):
		r = self.api.fetchFileHTTP( self.token, path, uri, username, password, auth, callbackid, priority, flags, expose_egress)
		logger.info( self.uid+" "+self.token+", fetchFileHTTP path "+path+" uri "+uri+" username "+str(username)+" auth "+str(auth)+" callbackid "+str(callbackid)+" priority "+str(priority)+" flags "+str(flags)+" expose_egress "+expose_egress+" = " + str(r) )
		return r

	def	fetchFileFTP(self, path, hostname, filename, username=None, password=None, port=21, passive=True, callbackid=0, priority=0, flags=0, expose_egress='COMPLETE'):
		r = self.api.fetchFileFTP( self.token, path, hostname, filename, username, password, port, passive, callbackid, priority, flags, expose_egress)
		logger.info( self.uid+" "+self.token+", fetchFileFTP path "+path+" hostname "+hostname+" filename "+filename+" username "+str(username)+" port "+str(port)+" passive "+str(passive)+" callbackid "+str(callbackid)+" priority "+str(priority)+" flags "+str(flags)+" expose_egress "+expose_egress+" = " + str(r) )
		return r

	def	fexists( self, path ):
		r = self.stat( path )
		logger.info( self.uid+" "+self.token+", fexists "+path+" = "+str(r) )
		if ((r['code'] == 0) and (r['type'] == 2)): return True
		else: return False

	def	dexists( self, path ):
		r = self.stat( path )
		logger.info( self.uid+" "+self.token+", dexists "+path+" = "+str(r) )
		if ((r['code'] == 0) and (r['type'] == 1)): return True
		else: return False

	def	exists(self, path):
		logger.info( self.uid+" "+self.token+", exists "+path )
		# +" = "+str(r) )
		if (self.fexists(path) or self.dexists(path)): return True
		else: return False

	def	mkdir(self, path, recursive = False):
		logger.info( self.uid+" "+self.token+", mkdir "+path )
		# +" = "+str(r) )
		if (not self.dexists(path)):
			if (recursive):
				r = self.makeDir2( path )
			else:
				r = self.makeDir( path )
			if (r == 0): 
				return True
			else: 
				return False
		else:	
			return False

	def	read(self, path):
		logger.info( self.uid+" "+self.token+", read "+self.mapper.url+urllib2.quote(path) )
		if (self.fexists(path)):
			response = urllib2.urlopen( self.mapperurl+urllib2.quote(path) )
			return response.read()
		else:
			return False

	def	post(self, source, destination, rename=None, mimetype='auto', mtime=None, egress_policy='COMPLETE', mkdir=False, callback=None):
		logger.info( self.uid+" "+self.token+", post "+source+" "+destination+", rename="+str(rename)+", mimetype="+str(mimetype)+", mtime="+str(mtime)+", egress="+str(egress_policy)+", mkdir="+str(mkdir))
		if (not os.path.isfile(source)): logger.info( "local("+source+") does not exist") ; return False 
		if (not self.dexists(destination)): logger.info( "remote("+destination+") does not exist") ; return False

		source_path = os.path.dirname(source) ; source_name = os.path.basename(source)
	
		poster.streaminghttp.register_openers()
	
		if callback<>None:
			datagen, headers = poster.encode.multipart_encode( {
				"uploadFile": open(source, "rb"),
				"directory": destination,
				"basename": source_name,
				"expose_egress": egress_policy
				}, cb=callback)
		else:
			datagen, headers = poster.encode.multipart_encode( {
				"uploadFile": open(source, "rb"),
				"directory": destination,
				"basename": source_name,
				"expose_egress": egress_policy
				} )

		request = Request(self.posturl, datagen, headers)
		request.add_header("X-Agile-Authorization", self.token)
		request.add_header("X-Content-Type", mimetype )

		try: result = urlopen(request).read()
		except HTTPError, e: logger.info( 'HTTP Error: '+str(e.code) ) ; return False
		except URLError, e: logger.info( 'URL Error: '+str(e.reason) ) ; return False

		return True

# End of agile.py
