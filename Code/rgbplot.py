import os
from os.path import join as pathjoin
import numpy as np
import scipy.misc as mi
try:
    from PIL import Image
except:
    from pillow import Image
from libtiff import TIFF
import matplotlib.pyplot as plt
import matplotlib.cm as cm
try:
    import pylab
except:
    from matplotlib import pylab
import gdal
import shutil

import ee_download
import Method2

def rgbPlot(image):
	files = os.listdir(image)
	for im in files:
		if im.endswith('.B3.tif'):
			b3 = gdal.Open(pathjoin(image,im), gdal.GA_Update).ReadAsArray()
		if im.endswith('.B4.tif'):
			b4 = gdal.Open(pathjoin(image,im), gdal.GA_Update).ReadAsArray()
		if im.endswith('.B5.tif'):
			b5 = gdal.Open(pathjoin(image,im), gdal.GA_Update).ReadAsArray()

	direc = image
	dirsplit = direc.split('/')
	n = len(dirsplit)
	folder = dirsplit[n-1]
	rgb = np.dstack((b5,b4,b3))
	my_dpi=100.0
	f = plt.figure(frameon = False)
	f.set_size_inches(rgb.shape[1]/my_dpi, rgb.shape[0]/my_dpi)

	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)

        #aspect='normal' is depracated in matplotlib
	ax.imshow(rgb, aspect='auto')
	f.savefig(pathjoin(image,folder+".rgb.tif"))
	plt.close()


def ndsi(image):
	files = os.listdir(image)

	for im in files:
		if im.endswith('.B2.tif'): 
			b2 = gdal.Open(pathjoin(image,im), gdal.GA_Update).ReadAsArray()
		if im.endswith('.B5.tif'): 
			b5 = gdal.Open(pathjoin(image,im), gdal.GA_Update).ReadAsArray()

	direc = image
	dirsplit = direc.split('/')
	n = len(dirsplit)
	folder = dirsplit[n-1]
	b2f = b2.astype(np.float)
	b5f = b5.astype(np.float)
	nrf = np.subtract(b2f, b5f)
	drf = np.add(b2f,b5f)
	np.seterr(divide='ignore', invalid='ignore')
	ndsi = np.divide(nrf,drf) 
	ndsi = np.nan_to_num(ndsi)
	ndsi1 = mi.bytescale(ndsi) # interpolate image to [0,255]
	ndsi_ind = np.int64(drf>0)
	ndsi1 = np.multiply(ndsi_ind, ndsi1)
	ndsi1 = mi.bytescale(ndsi1)
	tif = TIFF.open(pathjoin(image,folder+".ndsi.tif"), mode = 'w')
	tif.write_image(ndsi1)

def classifyLandsat(path, GlacierName, BoundingBox):
    landsatPath = pathjoin(path,"Data",GlacierName,"Landsat")
    Method2.classify(landsatPath,0.7,-21.153,0.176,0.550)
    images = [pathjoin(path,"Data",GlacierName,"Landsat",item) for item in os.listdir(pathjoin(path,"Data",GlacierName,"Landsat"))]
    for count, image in enumerate(images,start=1):
        if image.endswith('.zip'):
            continue
        print(str(count)+": "+image)
        try:
            rgbPlot(image)
            ndsi(image)
        except Exception, e:
            print("Error creating ndsi or rgbPlot for "+image)
            print(str(e))
            pass

def downloadLandsat(path, GlacierName, BoundingBox):
        bounds = ee_download.getBounds(float(BoundingBox[0]),float(BoundingBox[2]),float(BoundingBox[1]),float(BoundingBox[3]))
	ee_download.ee_download_Allbands(path,GlacierName,bounds)
	
