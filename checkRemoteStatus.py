#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Yuxiang Sun'

import paramiko
import threading
import socket
import os
import sys

#paramiko.util.log_to_file("/tmp/testparamiko")

def check_connection(ip):
	"""
	This function is used to test target server can be connected or not.
	If the IP can be connected, return IP address, else return False, and write the disconnected ip into ip_disconnect files.
	"""
	print 'Test: %s' %ip
	result = os.system('ping -c 1 -w 1 %s' %ip)
	result >>= 8
	#print result
	if (result == 0):
		print 'Server %s can be Connected!!!\n' %ip
#		os.system('echo %s > ip_can_connect' %ip)
		return ip
	elif(result == 1):
		print 'Server %s Connection Failed.\n' %ip
		os.system('echo %s >> ip_disconnect' %ip)
		return False

def check_port(ip,port):
	"""
	This function is used to test target server's port can be connected or not.
	If the port can be connected, return True, else return False.
	"""
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.settimeout(3)
	print 'Test: %s %s' %(ip,port)
	try:
		sock.connect((str(ip),int(port)))
		print 'Server %s port %d is Connected!!!\n' %(ip,port)
#		os.system('echo %ip > ip_can_ssh_connected' %ip)
		sock.close()
		return True
	except Exception:
		print 'Server %s Port %d Error\n' %(ip,port)
#		os.system('echo %s >> ip_can_connect_no_port' %ip)
		sock.close()
		return False

def check_passwd(ip,port,passwd):
	"""
	This function is used to check target server's password is correct or not.
	If the password is correct, return True, else return False.
	"""
	print 'Test: %s, %s, %s' %(ip,port,passwd)
	try:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(ip,int(port),'root',str(passwd))
		print 'The Password of Server %s is Correct!!!\n' %ip
#		os.system('echo %s >> ip_can_login' %ip)
		client.close()
		return True
	except:
		print 'Server %s Password Error\n' %ip
#		os.system('echo %s >> ip_no_passwd' %ip)
		client.close()
		return False

def test_ssh_connect(ip,port,passwd):
	"""
	This function is used to test target server's password
	"""
	try:
		test = paramiko.SSHClient()
		test.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		test.connect(ip,port,'root',passwd)
		print 'The Server %s of port %s can login SUCCESSFULLY!!!\n' %(ip,port)
		test.close()
		return True
	except:
		print 'The Server %s of port %s can NOT login\n' %(ip,port)
		test.close()
		return False


#if __name__=='__main__':
#	threads = []
#	ip="192.68.1.81"
#	passwd="BOChq999"
#	port=22
#	print 'Begin ... \n'
#	check_connection(ip)
#	check_passwd(ip,passwd)
#	check_port(ip,port)

#	th = threading.Thread(target = check_passwd,args = (ip,passwd))
#	th.start()
#	ch = threading.Thread(target = check_port,args = (ip,port))
#	ch.start()
