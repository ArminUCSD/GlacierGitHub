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


for row in range(2509,sheets[0].nrows-1):
    print sheets[0].cell(row,1).value, sheets[0].cell(row,0).value, sheets[0].cell(row,9).value, sheets[0].cell(row,10).value, sheets[0].cell(row,11).value, sheets[0].cell(row,12).value, sheets[0].cell(row,13).value
    if sheets[0].cell(row,11).value != "" and sheets[0].cell(row,12).value != " " and sheets[0].cell(row,13).value != "":
        sql_glaciers = """INSERT INTO wgms_glaciers VALUES("%s","%s",'%.6f','%.7f',%s,%s,%s);""" % \
           (sheets[0].cell(row,1).value, sheets[0].cell(row,0).value, sheets[0].cell(row,9).value, sheets[0].cell(row,10).value, sheets[0].cell(row,11).value, sheets[0].cell(row,12).value, sheets[0].cell(row,13).value)
    elif sheets[0].cell(row,11).value != "" and sheets[0].cell(row,13).value != "":
        sql_glaciers = """INSERT INTO wgms_glaciers(glacier_name,political_unit,latitude,longitude,primary_classification,frontal_characteristics) VALUES("%s","%s",'%.6f','%.7f',%s,%s);""" % \
           (sheets[0].cell(row,1).value, sheets[0].cell(row,0).value, sheets[0].cell(row,9).value, sheets[0].cell(row,10).value, sheets[0].cell(row,11).value, sheets[0].cell(row,13).value)
    elif sheets[0].cell(row,11).value != "" :
        sql_glaciers = """INSERT INTO wgms_glaciers(glacier_name,political_unit,latitude,longitude,primary_classification) VALUES("%s","%s",'%.6f','%.7f',%s);""" % \
           (sheets[0].cell(row,1).value, sheets[0].cell(row,0).value, sheets[0].cell(row,9).value, sheets[0].cell(row,10).value, sheets[0].cell(row,11).value)
    else:
        sql_glaciers = """INSERT INTO wgms_glaciers(glacier_name,political_unit,latitude,longitude) VALUES("%s","%s",'%.6f','%.7f');""" % \
           (sheets[0].cell(row,1).value, sheets[0].cell(row,0).value, sheets[0].cell(row,9).value, sheets[0].cell(row,10).value)
        
    print sql_glaciers
    try:
        cursor.execute(sql_glaciers)
        db.commit()
    except MySQLdb.Error as e:
        print e.args[0],e.args[1]
        db.rollback()
        print row,sheets[0].cell(row,1).value
        if e.args[0] != 1062:
            exit()
