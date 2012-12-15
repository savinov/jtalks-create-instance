import MySQLdb as mdb
import sys

def create(host, db_name, db_user, db_pass):
	connection = None
	try:
		connection = mdb.connect(host, db_user, db_pass)
		cursor = connection.cursor()
		sql = 'CREATE DATABASE ' + db_name + ' DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci'
		cursor.execute(sql)

	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

	finally:    
		if connection is not None:    
			connection.close()
