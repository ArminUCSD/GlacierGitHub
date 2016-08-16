import os
import MySQLdb
from xlwt import Workbook
from xlrd import open_workbook

db = MySQLdb.connect("localhost","root","ncsu","glaciers")
print "Connection Established"
cursor = db.cursor()
print "Cursor created"

workbook = open_workbook('/home/aseshad/RA/glacier_final_mat1.xls')
sheet = workbook.sheet_by_index(0)
book = Workbook()
sheet1 = book.add_sheet("glims_glaciers")
sheet1.write(0,0,"Glacier Name")
sheet1.write(0,1,"Area")
sheet1.write(0,2,"Ground records")

for row in range(0,sheet.nrows):
	glims_id = sheet.cell(row,0).value
	wg_name = sheet.cell(row,11).value 
	sql_query = 'select area from glaciers where glacier_id="%s";' % glims_id
	query = 'select * from front_variation where glacier_name="%s";' % wg_name
	print sql_query
	print query
	try:
		cursor.execute(sql_query)
        	r = cursor.fetchone()
		cursor.execute(query)
		r1 = cursor.fetchone()
        	sheet1.write(row+1,0,wg_name)
		if r:
        		sheet1.write(row+1,1,float(r[0]))
		if r1:
        		sheet1.write(row+1,2,"True")
		else:
        		sheet1.write(row+1,2,"False")
	except MySQLdb.Error as e:
		print e.args[0],e.args[1]
	        print "Error in fetching data"
##    sql_query = 'select * from points where glacier_id="%s";' % gid
##    print sql_query
##    try:
##        cursor.execute(sql_query)
##        results = cursor.fetchall()
##        i=2
##        for r in results:
##            sheet1.write(i,0,r[1])
##            sheet1.write(i,1,r[2])
##            i = i + 1
##    except:
##        print "Error in fetching points"
            
book.save('glacier_info_area_gr.xls')
db.close()
