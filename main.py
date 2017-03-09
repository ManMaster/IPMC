#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Yuxiang Sun'

import checkRemoteStatus
import paramiko
import threading
import os
import xlrd
from base64 import b64decode

#set the port and password here
passwd="BOChq9"
port=22

def check_manage_status(line,port,passwd):
	"""
	Loop to check ip status, and distribute each ip to different files.
	"""
	#check ip connection, if ip connection is ok, check the port.
	ip = checkRemoteStatus.check_connection(line)
	if ip is not False:
		#check port connection, if port connection is ok, check the password.
		#if the password is wrong, add ip into ip_can_connect_no_port file.
		if checkRemoteStatus.check_port(ip,port) is True:
			pass_status = checkRemoteStatus.test_ssh_connect(ip,port,passwd)
			#check password, if the password is correct, set ssh no password login, and add the ip into inventory.
			#if the password is wrong, add ip into ip_no_passwd file
			if pass_status is False:
				os.system('echo %s >> ip_no_passwd' %ip)
			elif pass_status is True:
				print '#########################################Password is OK#####################################\n'
				os.system('./login.exp %s %s' %(ip,passwd))
				os.system('echo %s >> inventory' %ip)
		else:
			os.system('echo %s >> ip_can_connect_no_port' %ip)


def ip_loop_manage_process(port,passwd):
	"""
	Loop to check status
	"""
	#open the file, read each line.
	fo_iplist = open("iplist","r")
	print '#################Begin to Check Remote Status###################\n'
	while True:
		line = fo_iplist.readline()
		line = line.strip()
		print line
		if not line:
			break
		else:
			check_manage_status(line,port,passwd)
#			#check ip connection, if ip connection is ok, check the port.
#			ip = checkRemoteStatus.check_connection(line)
#			if ip is not False:
#				#check port connection, if port connection is ok, check the password.
#				#if the password is wrong, add ip into ip_can_connect_no_port file.
#				if checkRemoteStatus.check_port(ip,port) is True:
#					pass_status = checkRemoteStatus.test_ssh_connect(ip,port,passwd)
#					#check password, if the password is correct, set ssh no password login, and add the ip into inventory.
#					#if the password is wrong, add ip into ip_no_passwd file
#					if pass_status is False:
#						os.system('echo %s >> ip_no_passwd' %ip)
#					elif pass_status is True:
#						print '#########################################Password is OK#####################################\n'
##						os.system('./login.exp %s %s' %(ip,passwd))
#						os.system('echo %s >> inventory' %ip)
#				else:
#					os.system('echo %s >> ip_can_connect_no_port' %ip)
			continue;
	fo_iplist.close()
	print '####################End Check Remote Status#####################\n'

def manage_ip_by_excel(hostfile = ''):
	host_excel = xlrd.open_workbook(filename=hostfile,verbosity=1,encoding_override='UTF-8')
	host_table = host_excel.sheets()[0]
	host_nrows = host_table.nrows	#get excel table rows

	for row in range(host_nrows):
		if row == 0:	#pass the first line
			continue
		hostname = host_table.row_values(row)[1]	#the second column is hostname
		ip = host_table.row_values(row)[2]		#the third column is ip address
		passwd_base64 = host_table.row_values(row)[4]	#the fifth column is password

#		password = b64decode(passwd_base64)		#decrypte password. In eirms.xls files, the passwd needs to decrypte before use.
#		print "%s,%s,%s\n" %(hostname,ip,password)
#		check_manage_status(ip,port,password)	#check the status

		print "%s,%s,%s\n" %(hostname,ip,passwd_base64)
		check_manage_status(ip,port,passwd_base64)
			

if __name__ == '__main__':

	manage_ip_by_excel('test.xls')
	#ip_loop_manage_process(port,passwd)

	#Multi-thread method 
#	t1 = threading.Thread(target=manage_ip_by_excel,args=('eirms.xls'))
#	t1.start()
