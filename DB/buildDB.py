import shapefile
import os
import MySQLdb


db = MySQLdb.connect("localhost","root","ncsu","glaciers")
print "Connection Established"
cursor = db.cursor()
print "Cursor created"

os.chdir('/home/aseshad/RA')
path = os.getcwd()+"/Glacier Data/glims_db_20140116/"
print path
sf = shapefile.Reader(path+"glims_polygons")
records = sf.records()
shapes  = sf.shapes()
for i in range(45700,len(records)):
	sql_glaciers = """INSERT INTO glaciers VALUES("%s","%s","%s","%s",'%.6f','%.6f','%.6f','%.6f');""" % \
		(records[i][2],records[i][14],records[i][15],records[i][0],shapes[i].bbox[0],shapes[i].bbox[1],shapes[i].bbox[2],shapes[i].bbox[3])
	print sql_glaciers
	try:
		#if records[i][0] == "glac_bound" or records[i][0] == "basin_bound":
		cursor.execute(sql_glaciers)
		db.commit()
		for points in shapes[i].points:
			sql_points = "INSERT INTO points VALUES('%s','%.6f','%.6f');" % \
				(records[i][2],points[0],points[1])
			cursor.execute(sql_points)
			db.commit()
	except MySQLdb.Error as e:
		print e.args[0],e.args[1]
		db.rollback()
		print i,records[i][2]
		if e.args[0] != 1062:
			exit()

db.close()


##count = 0
##for i in range(len(shapes)):
##    if records[i][2] == "G007800E45965N":
##        for points in shapes[i].points:
##            sql = "INSERT INTO POINTS VALUES('%s','%.6f','%.6f');" % \
##                  (records[i][2],points[0],points[1])
##            try:
##                if records[i][0] != "intrnl_rock":
##                    cursor.execute(sql)
##                    count = count+1
##                db.commit()
##            except:
##                print "error"
##                db.rollback()
##print count


