# ./recurse.py /Volumes/Music/Seeding/ /Test/


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
from AgileCLU import AgileCLU
from os.path import join, getsize

source_path = sys.argv[1] 
destination_path = sys.argv[2]

agile = AgileCLU( 'wylie' )

result = agile.makeDir( '/Test' )

for root, dirs, files in os.walk(source_path):
	print root.replace(source_path,"")+" -> "+destination_path+root.replace(source_path,""),
	result = agile.makeDir( destination_path+root.replace(source_path,"") )
	if result==0: print " = OK"
	elif result==-1: print " = MALFORMED PATH"
	elif result==-2: print " = DIRECTORY EXISTS"
	elif result==-3: print " = PARENT DOES NOT EXIST"

	# print root.replace(path,""), "consumes",
	# print sum(getsize(join(root, name)) for name in files),
	# print "bytes in", len(files), "non-directory files"
	if 'CVS' in dirs:
		dirs.remove('CVS')  # don't visit CVS directories

agile.logout()
