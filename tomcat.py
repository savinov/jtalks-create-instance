#!/usr/bin/python

from xml.dom.minidom import parse
from optparse import OptionParser
import os
import MySQLdb as mdb
import sys

def install(instance_name, port):
	temp_dir = "/tmp"
	dist_file_name = "apache-tomcat-6.0.32.tar.gz"
	dist_dir_name = "apache-tomcat-6.0.32"
	dist_url = "http://archive.apache.org/dist/tomcat/tomcat-6/v6.0.32/bin/" + dist_file_name
	instance_dir = "~/instances/" + instance_name
	base_port = int(port)

	# download distribution and unpack it
	os.system("rm -rf " + instance_dir)
	os.system("mkdir -p " + "~/instances")
	os.chdir(temp_dir)
	os.system("rm -rf " + dist_file_name)
	os.system("rm -rf " + dist_dir_name)
	os.system("wget " + dist_url)
	os.system("tar xzvf " + dist_file_name)
	os.system("mv " + dist_dir_name + " " + instance_dir)

	# create a backup of original configuration
	os.chdir(os.path.expanduser(instance_dir) + "/conf")
	new_file_name = "server.xml"
	old_file_name = new_file_name + ".backup"
	os.rename(new_file_name, old_file_name)

	# change port attributes
	doc = parse(old_file_name)
	node = doc.getElementsByTagName('Connector')
	node[0].setAttribute('port', str(base_port))
	node[0].setAttribute('redirectPort', str(base_port + 1))
	node[1].setAttribute('port', str(base_port + 2))
	node[1].setAttribute('redirectPort', str(base_port + 1))
	node = doc.getElementsByTagName('Server')
	node[0].setAttribute('port', str(base_port + 3))

	# persist changes to the new configuration
	xml_file = open(new_file_name, "w")
	doc.writexml(xml_file, encoding="utf-8")
	xml_file.close()

