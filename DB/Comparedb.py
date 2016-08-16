import os
import MySQLdb
##from xlwt import Workbook
import csv

db = MySQLdb.connect("localhost","root","AdiSesh","glaciers")
print "Connection Established"
cursor = db.cursor()
print "Cursor created"

##book = Workbook()
##sheet1 = book.add_sheet("Glacier Matching")
##sheet1.write(0,0,"Glacier ID")
##sheet1.write(0,1,"Glacier Name")
##sheet1.write(0,2,"WGMS ID")
##sheet1.write(0,3,"Line type")
##sheet1.write(0,4,"Left Bottom X")
##sheet1.write(0,5,"Left Bottom Y")
##sheet1.write(0,6,"Right Top X")
##sheet1.write(0,7,"Right Top Y")
##sheet1.write(0,8,"Location X")
##sheet1.write(0,9,"Location Y")
##sheet1.write(0,10,"Location Z")
##sheet1.write(0,11,"WGMS Name")
##sheet1.write(0,12,"Political Unit")
##sheet1.write(0,13,"Latitude")
##sheet1.write(0,14,"Longitude")
##sheet1.write(0,15,"Primary Classification")
##sheet1.write(0,16,"Form")
##sheet1.write(0,17,"Frontal Characteristics")
query = """select * from glaciers as g,wgms_glaciers as wg where (wg.longitude between g.left_bottom_x and g.right_top_x) and (wg.latitude between g.left_bottom_y and g.right_top_y);"""

try:
    cursor.execute(query)
    rows = cursor.fetchall()
except:
    print "Error in fetching records"
print "fetched records", len(rows)

with open("glacier_match.csv","w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
##    sheet1.write(count,0,row[0].encode("UTF-8"))
##    sheet1.write(count,1,row[1].encode("UTF-8"))
##    sheet1.write(count,2,row[2].encode("UTF-8"))
##    sheet1.write(count,3,row[3].encode("UTF-8"))
##    sheet1.write(count,4,row[4])
##    sheet1.write(count,5,row[5])
##    sheet1.write(count,6,row[6])
##    sheet1.write(count,7,row[7])
##    sheet1.write(count,8,row[8])
##    sheet1.write(count,9,row[9])
##    sheet1.write(count,10,row[10])
##    sheet1.write(count,11,row[11].encode("UTF-8"))
##    sheet1.write(count,12,row[12].encode("UTF-8"))
##    sheet1.write(count,13,row[13])
##    sheet1.write(count,14,row[14])
##    sheet1.write(count,15,row[15])
##    sheet1.write(count,16,row[16])
##    sheet1.write(count,17,row[17])
##    count=count+1
##    
##book.save("glacier_match.xls")
db.close()

