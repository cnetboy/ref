#!/usr/bin/env python		

# coding: utf8		
	

import sys,argparse
import pyjsonrpc
from subprocess import call		
		
class remote_installer():		
		
	def __init__(self):		
		#Setup address range to send to 201225		
		self.clients = range(201,225)		
		
	def run(self):	

	    	parser = argparse.ArgumentParser()		
	    	parser.add_argument('path', help='file you want to copy to remote nodes')
		self.args = parser.parse_args()
    		for x in self.clients:
			command = "scp -i /home/ubuntu/spart.key "+self.args.path+" ubuntu@192.168.1."+str(x)+":/home/ubuntu/"
			print command
			call(command, shell=True)	
remote_installer().run()		
		
		
			
# Notifications send messages to the server, without response.		
#http_client.notify("do_command", "touch hello.txt") 		
