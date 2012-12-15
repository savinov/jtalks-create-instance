#!/usr/bin/python

from optparse import OptionParser
import tomcat
import mysql
import nginx

# parameters for DB and nginx
db_host = "localhost"
db_user = "root"
db_pass = "123"
nginx_host = "jtalks.org"
nginx_user = "nginxconf"
nginx_key_file = "/home/tomcat/.ssh/id_rsa"

# parse command-line arguments
parser = OptionParser()
parser.add_option("-n", "--name", dest="instance_name",
                  help="instance NAME", metavar="NAME")
parser.add_option("-p", "--port", dest="port",
                  help="port number for Tomcat server", metavar="PORT")
(options, args) = parser.parse_args()

# install tomcat, create database and configure nginx
tomcat.install(options.instance_name, options.port)
mysql.create(db_host, options.instance_name, db_user, db_pass)
nginx.add(nginx_host, nginx_user, nginx_key_file, options.instance_name, options.port)
nginx.restart(nginx_host, nginx_user, nginx_key_file)

