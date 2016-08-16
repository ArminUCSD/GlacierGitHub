import os
from os.path import join as pathjoin
import rpy2.robjects as robjects
from rpy2.robjects.numpy2ri import numpy2ri
try:
    from PIL import Image
except:
    from pillow import Image

import gdal
import numpy
robjects.numpy2ri.activate()

def arcLengthVector(pathVector, stepSize, resolution):
	arcVector = []
	for i in range(len(pathVector)):
		arcVector.append(round(i*stepSize*resolution,1));
	# print len(pathVector), len(arcVector)
	return arcVector

def isLeap(year):
	if ((year%100==0 and year%400==0) or (year%100!=0 and year%4==0)):
		return 1
	return 0

def intensityProfile(imagespath,path,Input,pmissing,weights):
	robjects.r('''source('IntensityProfile.r')''')
	r_ip = robjects.globalenv['IPBL']
	timeline = []
	landsatFiles = {}
	IPTimeSeries = {}
	for images in os.listdir(imagespath):
		for fn in os.listdir(pathjoin(imagespath,images)):
			if fn.endswith('.'+Input+'.tif') or (Input == "B6_VCID_1" and fn.endswith('.B6.tif')):
				time = int(fn[9:13])
				if(isLeap(int(fn[13:16]))):
					time = time + int(fn[13:16])/366.0
				else:
					time = time + int(fn[13:16])/365.0
				if(time not in timeline):
					landsat = gdal.Open(pathjoin(imagespath,images,fn), gdal.GA_Update).ReadAsArray()
					landsat = numpy.int_(landsat)
					rotlandsat = numpy.rot90(landsat,3)
					where_are_nan = numpy.isnan(rotlandsat) # this is questionable? there is really nan?
					rotlandsat[where_are_nan] = 0
					IP = r_ip(rotlandsat,path,pmissing,weights)
					IParray = numpy.asarray(IP)
					if numpy.sum(IParray) > 0:
						timeline.append(time)
						IPTimeSeries[timeline[-1]] = IP
						landsatFiles[timeline[-1]] = pathjoin(imagespath,images,fn)
	return (timeline,IPTimeSeries,landsatFiles)

