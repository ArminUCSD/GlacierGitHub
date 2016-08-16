import os
import MySQLdb
import xlrd


db = MySQLdb.connect("localhost","root","ncsu","glaciers")
print "Connection Established"
cursor = db.cursor()
print "Cursor created"

book = xlrd.open_workbook('../../glims_points.xlsx')
sheet = book.sheet_by_index(0)

for row in range(2,sheet.nrows-1):
    sql_glaciers = """update glaciers set location_x = %.6f, location_y = %.6f, location_z = %.6f where glacier_id = "%s";""" % \
                   (sheet.cell(row,0).value, sheet.cell(row,1).value, sheet.cell(row,2).value, sheet.cell(row,3).value)

    print sql_glaciers
    try:
        cursor.execute(sql_glaciers)
        db.commit()
    except MySQLdb.Error as e:
        print e.args[0],e.args[1]
        db.rollback()
        print row
        exit()



    
