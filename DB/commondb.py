import xlrd
import os
import MySQLdb


db = MySQLdb.connect("localhost","root","ncsu","glaciers")
print "Connection Established"
cursor = db.cursor()
print "Cursor created"

os.chdir('/home/aseshad/RA')
book = xlrd.open_workbook('glacier_final_match.xls')
sheet = book.sheet_by_index(0)

for row in range(1,sheet.nrows):
	print sheet.cell(row,0).value, sheet.cell(row,1).value, sheet.cell(row,11).value, sheet.cell(row,18).value
	sql = """INSERT INTO commonDB VALUES("%s","%s","%s",'%.6f');""" % \
		(sheet.cell(row,0).value, sheet.cell(row,1).value, sheet.cell(row,11).value, sheet.cell(row,18).value)

	print sql

	try:
		cursor.execute(sql)
		db.commit()
	except MySQLdb.Error as e:
		print e.args[0],e.args[1]
		db.rollback()
		print row,sheets[0].cell(row,1).value
		if e.args[0] != 1062:
			exit()