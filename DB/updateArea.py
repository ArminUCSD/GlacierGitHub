import os
import MySQLdb
import xlrd


db = MySQLdb.connect("localhost","root","ncsu","glaciers")
print "Connection Established"
cursor = db.cursor()
print "Cursor created"

sql = "select * from glaciers;"
cursor.execute(sql)
table = cursor.fetchall()
print len(table)
print table[0]
for row in table:
	area = (row[6] - row[4]) * (row[7] - row[5])
	sql_glaciers = """update glaciers set area = %.6f where glacier_id = "%s";""" % \
				(area, row[0])


	print sql_glaciers
	try:
		cursor.execute(sql_glaciers)
		db.commit()
	except MySQLdb.Error as e:
		print e.args[0],e.args[1]
		db.rollback()
		print row
		exit()



    
