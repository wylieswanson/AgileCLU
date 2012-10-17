import jsonrpclib
import ConfigParser, sys, os.path, logging
import poster 
import pyDes, hashlib, base64
from urllib2 import Request, urlopen, URLError, HTTPError
import progressbar

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logger = logging.getLogger('AgileCLU')
logger.addHandler(NullHandler())
cfg = ConfigParser.ConfigParser() 

def	epwbasekey( username, proto, hostname, basepath ):
	m = hashlib.md5()
	m.update( username )
	m.update( proto )
	m.update( hostname )
	m.update( basepath )
	key = base64.b64encode(hashlib.sha256( m.digest() ).digest())
	return key[0:24]

def	e_pw_hash( str, username, proto, hostname, basepath ):
	hash = base64.b64encode(pyDes.triple_des(epwbasekey(username,proto,hostname,basepath)).encrypt(str, padmode=2))
	return hash

def	e_pw_dehash( str, username, proto, hostname, basepath ):
	basekey=epwbasekey(username,proto,hostname,basepath)
	try:
		b64decode=base64.b64decode(str)
	except TypeError, ValueError:
		b64decode="12345678"
	try:
		if (len(b64decode) % 8 == 0):
			dehash = pyDes.triple_des(basekey).decrypt(b64decode, padmode=2)
		else:
			print "Password corruption - not Base-64 compliant.  Delete the profile and create a new one."
			sys.exit(1)
	except TypeError, ValueError:
		dehash = "87654321"
	if dehash is '': dehash='87654321' 
	return dehash

class	AgileCLU:
	__module__ = "AgileCLU"
	__version__ = "0.4.1"

	def     __init__(self, profile='default'):
		config_path = os.path.expanduser( '~/.agileclu/' )

		# Load configuration variables

		if os.path.isfile( os.path.join( config_path, profile+'.conf' ) ):
			cfg.read( os.path.join( config_path, profile+'.conf' ) )

		else:
			print "Profile (%s) does not exist.  Use \"agileprofile create %s\" to create the profile." % (profile,profile)
			# logger.critical( "configuration /etc/agile/"+profile+".conf does not exist" )
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
		self.postmultiurl = self.ingest_protocol + ":8080//" + self.ingest_hostname + "/multipart"

		self.pbar = None
		self.pbarfname = None

		upw = e_pw_dehash( cfg.get("Identity", "password"), self.uid, self.egress_protocol, self.egress_hostname, self.egress_basepath )

		if upw is "87654321":
			print "Password corruptions - dehash was empty!  Delete the profile and create a new one."
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

	def	postmultiurlstr(self):
		logger.info( self.uid+" "+self.token+", postmultiurl="+self.postmultiurl )
		return self.postmultiurl

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

	def	createMultipart(self, path):
		r = self.api.createMultipart( self.token, path)
		logger.info( self.uid+" "+self.token+", createMultipart "+path )
		return r

	def	createMultipartPiece(self, mpid='', number=0, size=0, checksum='', uri=''):
		r = self.api.createMultipartPiece( self.token, mpid, number, size, checksum, uri )
		logger.info( self.uid+" "+self.token+", createMultipartPiece mpid " + mpid + " number " + str(number) + " size " + str(size) + " checksum " + checksum + " uri " + uri )

	def	completeMultipart( self, mpid='' ):
		r = self.api.completeMultipart( self.token, mpid )
		logger.info( self.uid+" "+self.token+", completeMultipart " + mpid )
		return r

	def	getMultipartStatus( self, mpid='' ):
		r = self.api.getMultipartStatus( self.token, mpid )
		logger.info( self.uid+" "+self.token+", getMultipartStatus " + mpid )
		return r

	def	listMultipartPiece( self, mpid='', lastpiece=0, pagesize=100 ):
		r = self.api.listMultipartPiece( self.token, mpid, lastpiece, pagesize )
		logger.info( self.uid+" "+self.token+", listMultipartPiece " + mpid + " lastpiece " +str(lastpiece)+ " pagesize "+ str(pagesize) )
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

	def	pbar_callback(self, param, current, total):
		if (self.pbar==None):
			widgets = [ unicode(self.pbarfname, errors='ignore').encode('utf-8'), ' ', progressbar.FileTransferSpeed(), ' [', progressbar.Bar(), '] ', progressbar.Percentage(), ' ', progressbar.ETA() ]
			self.pbar = progressbar.ProgressBar( widgets=widgets, maxval=total ).start()
		try:
			self.pbar.update(current)
		except AssertionError, e:
			print e
			print "!"

	def	post(self, sourceObject, targetPath, rename=None, mimetype='auto', mtime=None, egress_policy='COMPLETE', mkdir=False, callback=None):
		logger.info( self.uid+" "+self.token+", post "+sourceObject+" "+targetPath+", rename="+str(rename)+", mimetype="+str(mimetype)+", mtime="+str(mtime)+", egress="+str(egress_policy)+", mkdir="+str(mkdir))
		if (not os.path.isfile(sourceObject)): logger.info( "local("+sourceObject+") does not exist") ; return False 
		if (not self.dexists(targetPath)): logger.info( "remote("+targetPath+") does not exist") ; return False

		sourcePath = os.path.dirname(sourceObject) 
		sourceName = os.path.basename(sourceObject)
		self.pbarfname = sourceName
	
		poster.streaminghttp.register_openers()
	
		datagen, headers = poster.encode.multipart_encode( {
			"uploadFile": open( os.path.join(sourcePath,sourceName), "rb"),
			"directory": targetPath,
			"basename": sourceName,
			"expose_egress": egress_policy
			}, cb=callback)

		request = Request(self.posturl, datagen, headers)

		request.add_header("X-Agile-Authorization", self.token)
		request.add_header("X-Content-Type", mimetype )

		success = False ; attempt = 0
		while not success:
			attempt += 1
			try: 
				result = urlopen(request).read() 
				if callback<>None: self.pbar.finish()
				self.pbar = None
				success = True
			except HTTPError, e: 
				if callback<>None: self.pbar.finish()
				print '[!] HTTP Error: ', e.code
				self.pbar = None
				success = False
			except URLError, e: 
				if callback<>None: self.pbar.finish()
				print '[!] URL Error: ', e.reason
				self.pbar = None
				success = False
