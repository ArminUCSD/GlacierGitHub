#!/bin/python
import os, zipfile, logging, ee , urllib2, datetime, gdal
from os.path import join as pathjoin 
from os.path import exists as pathexists 
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# modified July 20, 2014 
import glob
import xlrd

try:
    from PIL import Image
except:
    from Pillow import Image
import xml.etree.ElementTree as treeObj
from xml.dom.minidom import parseString,parse

BASEIMAGE = 'srtm90_v4'
INITIALCRS = 30 
INITIALSCALE = 'EPSG:4326'
ELEVATIONTIFNAME = "srtm90_v4.elevation.tif"
USGSIMAGE = 'USGS/GMTED2010'

DEMFILE1 = "GMTED2010.be75.tif"
DEMFILE2 = "srtm90_v4.elevation.tif"

MY_SERVICE_ACCOUNT = '384403807661@developer.gserviceaccount.com'
MY_PRIVATE_KEY_FILE = 'Code/GoogleKey.pem'

def getBounds(MaxLon,MinLon,MaxLat,MinLat):
	LonLen = MaxLon-MinLon
	LatLen = MaxLat-MinLat
	MaxLon1 = MaxLon + margin*LonLen
	MinLon1 = MinLon - margin*LonLen
	MaxLat1 = MaxLat + margin*LatLen
	MinLat1 = MinLat - margin*LatLen
	bounds = [[MinLon1,MinLat1],[MaxLon1,MinLat1],[MaxLon1,MaxLat1],[MinLon1,MaxLat1]]
	return bounds

def getDLPath(image, region, scale=INITIALSCALE, crs=INITIALCRS):
    return image.getDownloadUrl({
        'scale': scale,
        'crs': crs,
        'region': region,
        })

def ee_download_DEM(path,glacier,bounds):
        keyfile = pathjoin(path, MY_PRIVATE_KEY_FILE)
	# define margin added to bounding box for downloading image 
	margin = 0.1
	folder = pathjoin(path,"Data")
	
	#-----------------------------------------------------------------------
	#                         access EE
	#-----------------------------------------------------------------------
        credentials = ee.ServiceAccountCredentials(MY_SERVICE_ACCOUNT, keyfile)
	ee.Initialize(credentials)
	
	print(glacier)
	glacier = glacier.encode('ascii','ignore')

	newpath = pathjoin(folder,glacier)
	if not pathexists(newpath): os.makedirs(newpath)

	#-----------------------------------------------------------------------
	#                        download DEM
	#-----------------------------------------------------------------------
	try:	
		image = ee.Image(BASEIMAGE)
                dlPath = getDLPath(image, bounds)
		demzip = urllib2.urlopen(dlPath)
		# download the zip file to document folder 
		workingDir = newpath
		if not pathexists(workingDir):
			os.mkdir(workingDir)
		with open(workingDir + '.zip', "wb") as local_file:
			local_file.write(demzip.read())
		# unzip the contents
		zfile = zipfile.ZipFile(workingDir + '.zip')
		for j in zfile.namelist():
			fd = open(pathjoin(workingDir,j),"w")
			fd.write(zfile.read(j))
			fd.close()
		# delete the zip file
		os.remove(workingDir + '.zip')
		DEM = np.array(gdal.Open(pathjoin(workingDir,ELEVATIONTIFNAME)).ReadAsArray())
		count = np.count_nonzero(DEM)
		if count == 0:
			os.remove(pathjoin(workingDir,ELEVATIONTIFNAME))
			image = ee.Image(USGSIMAGE)
			dlPath = getDLPath(image, bounds)
                        demzip = urllib2.urlopen(dlPath)
			if not pathexists(workingDir):
				os.mkdir(workingDir)
			with open(workingDir + '.zip', "wb") as local_file:
				local_file.write(demzip.read())
			# unzip the contents
			zfile = zipfile.ZipFile(workingDir + '.zip')
			for j in zfile.namelist():
				fd = open(pathjoin(workingDir,j),"w")
				fd.write(zfile.read(j))
				fd.close()
			# delete the zip file
			os.remove(workingDir + '.zip')
			return DEMFILE1 
		else:
			return DEMFILE2 

	except Exception, e:
		print("Download DEM")
		print(str(e))
		pass

def ee_download_Allbands(path,glacier,bounds):
        keyfile = pathjoin(path, MY_PRIVATE_KEY_FILE)
	# define margin added to bounding box for downloading image 
	margin = 0.1
	folder = pathjoin(path,"Data")
	
	#-----------------------------------------------------------------------
	#                         access EE
	#-----------------------------------------------------------------------
	ee.Initialize(ee.ServiceAccountCredentials(MY_SERVICE_ACCOUNT, keyfile))

	#------------------------------------------------------------------------
	#                       download L7 images from EE
	#------------------------------------------------------------------------
	# define time period of images
	beg_date = datetime.datetime(1999,1,1)
	end_date = datetime.datetime(2014,1,1)
	collection = ee.ImageCollection('LE7_L1T').filterDate(beg_date,end_date)
	polygon = ee.Feature.MultiPolygon([[bounds]])
	collection = collection.filterBounds(polygon)
	metadata = collection.getInfo()
	print(metadata.keys())
	print(metadata['features'][0]['id'])

	newpath = pathjoin(folder,glacier,"Landsat")
	if not pathexists(newpath): os.makedirs(newpath)

	#------------------------------------------------------------------------
	#                      download Band 61 of the Landsat
	#-----------------------------------------------------------------------

	for i in range(len(metadata['features'])):
		try:
			sceneName = metadata['features'][i]['id']
			print(sceneName + ': Scene ' + str(i+1) + ' of ' + str(len(metadata['features'])))
			workingScene = ee.Image(sceneName)
			dlPath = workingScene.getDownloadUrl({
				'scale': 30,
				'bands':[{'id':'B6_VCID_1'},{'id':'B5'},{'id':'B4'},{'id':'B3'},{'id':'B2'}],
				'crs': 'EPSG:4326',
				'region': bounds,
			})
			scenezip = urllib2.urlopen(dlPath)
			# download the zip file to documnet folder
			workingDir = pathjoin(newpath,sceneName.split('/')[1])
			if not pathexists(workingDir):
				os.mkdir(workingDir)
			with open(workingDir + '.zip', "wb") as local_file:
				local_file.write(scenezip.read())
			# unzip the contents
			zfile = zipfile.ZipFile(workingDir + '.zip')
			for j in zfile.namelist():
				jstring = j.encode('ascii','ignore')
				jsp = jstring.split(".")
				if jsp[2] =='tif':
					fd = open(pathjoin(workingDir,j),"w")
					fd.write(zfile.read(j))
					fd.close()
					
			# delete the zip file
			os.remove(workingDir + '.zip')

		except Exception, e:
                        print('Download band 61')
                        print(str(e))
			pass

	#------------------------------------------------------------------------
	#                       download L5 images from EE
	#------------------------------------------------------------------------
	# define time period of images
	beg_date = datetime.datetime(1984,1,1)
	end_date = datetime.datetime(2012,5,5)
	collection = ee.ImageCollection('LT5_L1T').filterDate(beg_date,end_date)
	polygon = ee.Feature.MultiPolygon([[bounds]])
	collection = collection.filterBounds(polygon)
	metadata = collection.getInfo()
	print(metadata.keys())
	print(metadata['features'][0]['id'])

	newpath = pathjoin(folder,glacier,"Landsat")
	if not pathexists(newpath): os.makedirs(newpath)

	#------------------------------------------------------------------------
	#                      download Band 6 of the Landsat
	#-----------------------------------------------------------------------

	for i in range(len(metadata['features'])):
		try:
			sceneName = metadata['features'][i]['id']
			print(sceneName + ': Scene ' + str(i+1) + ' of ' + str(len(metadata['features'])))
			workingScene = ee.Image(sceneName)
			dlPath = workingScene.getDownloadUrl({
				'scale': 30,
				'bands':[{'id':'B6'},{'id':'B5'},{'id':'B4'},{'id':'B3'},{'id':'B2'}],
				'crs': 'EPSG:4326',
				'region': bounds,
			})
			scenezip = urllib2.urlopen(dlPath)
			# download the zip file to documnet folder
			workingDir = pathjoin(newpath,sceneName.split('/')[1])
			if not pathexists(workingDir):
				os.mkdir(workingDir)
			with open(workingDir + '.zip', "wb") as local_file:
				local_file.write(scenezip.read())
			# unzip the contents
			zfile = zipfile.ZipFile(workingDir + '.zip')
			for j in zfile.namelist():
				jstring = j.encode('ascii','ignore')
				jsp = jstring.split(".")
				if jsp[2] =='tif':
					fd = open(pathjoin(workingDir, j),"w")
					fd.write(zfile.read(j))
					fd.close()
					
			# delete the zip file
			os.remove(workingDir + '.zip')

		except:
                        print('Download Band 6')
                        print(str(e))
			pass

	#------------------------------------------------------------------------
	#                       download L4 images from EE
	#------------------------------------------------------------------------
	# define time period of images
	beg_date = datetime.datetime(1982,8,22)
	end_date = datetime.datetime(1993,12,14)
	collection = ee.ImageCollection('LT4_L1T').filterDate(beg_date,end_date)
	polygon = ee.Feature.MultiPolygon([[bounds]])
	collection = collection.filterBounds(polygon)
	metadata = collection.getInfo()
	print(metadata.keys())
	print(metadata['features'][0]['id'])

	newpath = pathjoin(folder,glacier,"Landsat")
	if not pathexists(newpath): os.makedirs(newpath)

#ee_download('/home/aseshad/RA/Pipeline/','Rhonegletscher',7.881253,7.707613,45.985001,45.916481)

