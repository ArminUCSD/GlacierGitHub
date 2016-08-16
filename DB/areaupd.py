import os
import MySQLdb
import xlrd

book = xlrd.open_workbook("/home/aseshad/RA/glacier_final_match.xls")
sheet = book.sheet_by_index(0)

for row in range(sheet.nrows):
	gid = sheet.cell(row,0).value

	db = MySQLdb.connect("localhost","root","ncsu","glaciers")
	cursor = db.cursor()

	sql_query = 'select area from glaciers where glacier_id = "'+ gid+'" order by area desc;'
	try:
		cursor.execute(sql_query)
		r = cursor.fetchone()
	except MySQLdb.Error as e:
		print e.args[0],e.args[1]
		print "Error in fetching data"
	db.close()

	print r[0]