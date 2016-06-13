#!/usr/bin/env python		
# coding: utf8		
import sys,argparse		
import pyjsonrpc
import time
import json		
import threading		
class remote():		
		
	def __init__(self):
		self.clientConnections = [] 		
		#Setup address range to send to 201225		
		'''self.clients = range(201,225)		
		self.clientConnections = []		
		for x in self.clients:		
			self.clientConnections.append(pyjsonrpc.HttpClient(		
			    url = "http://192.168.1.%s:8080" % x,		
			    username = "mininet",		
			    password = "mininet"		
				))	'''	
	
		self.parser = argparse.ArgumentParser()
            #parser.add_argument('integers', metavar='R1 R2', type=int, nargs='2', help='select range of ips like 1 255')               
            #parser.add_argument('v', dest='verbose', action='store_true')              
            	self.parser.add_argument('command', help='command you want to run on remote nodes')
            	self.parser.add_argument('range', default=[], nargs='*')
		self.read_config()



	def read_config(self):
		with open("config.json") as json_file:
	    		json_data = json.load(json_file)
	                self.parser.add_argument('--'+json_data['options'][0]['name'], dest='u'+json_data['options'][0]['name'], default=[],action='store_true')
                        self.parser.add_argument('--'+json_data['options'][1]['name'], dest='u'+json_data['options'][1]['name'], default=[],action='store_true')
                        self.parser.add_argument('--'+json_data['options'][2]['name'], dest='u'+json_data['options'][2]['name'], default=[],action='store_true')
                        self.parser.add_argument('--'+json_data['options'][3]['name'], dest='u'+json_data['options'][3]['name'], default=[],action='store_true')
	                self.args = self.parser.parse_args()
			if self.args.ubackground:
				for addr in json_data['options'][0]['addresses']:
					self.clientConnections.append(pyjsonrpc.HttpClient(             
                            			url = "http://"+addr+":8080" ))   
			if self.args.u360:
				for addr in json_data['options'][1]['addresses']:
                                        self.clientConnections.append(pyjsonrpc.HttpClient(
                                                url = "http://"+addr+":8080" ))

			if self.args.u720:
				for addr in json_data['options'][2]['addresses']:
                                        self.clientConnections.append(pyjsonrpc.HttpClient(
                                                url = "http://"+addr+":8080" ))

			if self.args.u1080:
				for addr in json_data['options'][3]['addresses']:
                                        self.clientConnections.append(pyjsonrpc.HttpClient(
                                                url = "http://"+addr+":8080" ))


	def run(self):		
	    self.args = self.parser.parse_args()		
	    response = ""		
	    print "Client list \n==========="
	    for connection in self.clientConnections:		
	    	print connection.url		
	    	
		t = threading.Thread(target=self.send_and_wait, args=[connection])
	      #  t = threading.Thread(target=send_and_wait, args=(connection))
		# threads.append(t)
		t.start()

                response = connection.call("do_command", "tail -n 1 /home/ubuntu/nohup.out")
                if "200" in response:
                    response = '\033[92m'+"[OK]"+"\x1b[0m"
                else:
                    response = "'\033[91m'"+"[FAIL]"+"\x1b[0m"
                report = str(connection.url) + '::=' + response
                sys.stdout.write('\x1b[0m')
                print report
                sys.stdout.write('\x1b[0m')



		# response = connection.call("do_command", self.args.command)		
	#	connection.notify("do_command", self.args.command)
	    print 'Calls sent\n\n' 			
	    '''sys.stdout.write('\033[0m')'''
	def send_and_wait(self,connection):
	    response = connection.call("do_command", self.args.command)
    	    time.sleep(3)
	    print response
remote().run()		
		
		
			
# Notifications send messages to the server, without response.		
#http_client.notify("do_command", "touch hello.txt") 		
