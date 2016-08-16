import xlrd
import os
import MySQLdb


db = MySQLdb.connect("localhost","root","ncsu","glaciers")
print "Connection Established"
cursor = db.cursor()
print "Cursor created"

os.chdir('/home/aseshad/RA')
book = xlrd.open_workbook('Global_Terminus_Variation.xls')
sheets = []
for s in book.sheets():
    sheets.append(book.sheet_by_name(s.name))


for row in range(7,sheets[2].nrows-1):
    try:  
        print sheets[2].cell(row,1).value, sheets[2].cell(row,4).value, sheets[2].cell(row,5).value, sheets[2].cell(row,3).value
        if sheets[2].cell_type(row,4) != xlrd.XL_CELL_EMPTY and sheets[2].cell_type(row,5) != xlrd.XL_CELL_EMPTY:
            sql_glaciers = """INSERT INTO front_variation VALUES("%s",%s,%s,%s);""" % \
               (sheets[2].cell(row,1).value, sheets[2].cell(row,4).value, sheets[2].cell(row,5).value, int(sheets[2].cell(row,3).value))
            print sql_glaciers
            cursor.execute(sql_glaciers)
        elif sheets[2].cell_type(row,4)!= xlrd.XL_CELL_EMPTY:
            sql_glaciers = """INSERT INTO front_variation(glacier_name,front_variation,year) VALUES("%s",%s,%s);""" % \
               (sheets[2].cell(row,1).value, sheets[2].cell(row,4).value, int(sheets[2].cell(row,3).value))
            print sql_glaciers
            cursor.execute(sql_glaciers)
        db.commit()
    except MySQLdb.Error as e:
        print e.args[0],e.args[1]
        db.rollback()
        print row
        if e.args[0] != 1062:
            exit()
