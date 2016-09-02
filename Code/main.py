import os
from os.path import join as pathjoin
import fnmatch
import glob
try:
    from PIL import Image
except:
    from pillow import Image

import querydb
import ee_download
import Method1
import Method2
import Method3
import Method4
import TI
import rgbplot


DEMFILE1 = "GMTED2010.be75.tif"
DEMFILE2 = "srtm90_v4.elevation.tif"

STEPSIZE = 0.2
RESOLUTION = 30

def find(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result = os.path.join(root, name)
    return result

# General parameters
GlacierID=""
GlacierNames = ["Athabasca Glacier"]
GlacierNames1= ["Chaba Glacier","COXE","David Glacier","Fassett","Fox, Explorer","Litian glacier","North Canoe Glacier","CORBASSIERE GLACIER DE","FERPECLE GLACIER DE","FIESCHERGLETSCHER VS","Findelengletscher","FORNO VADREC DEL","FRANZ JOSE","GAULIGLETSCHER","GORNERGLETSCHER","GROSSER ALETSCH GLETSCHER","MONT MINE GLACIER DU","MORTERATSCH VADRET DA","OTEMMA","Rhonegletscher","Ferebee","Fraenkel","Mer de Glace","MURCHISON","Torre"]


imageInv = ["B2","B3","B4","ndsi"]
noImageInv = ["B5","B6_VCID_1","61"]
Input = "B6_VCID_1"  #from the above list of bands
classification = "algorithm"   #algorithm or manual
flowline = "median"  #regular or median
numParallel = 0   #number of parallel paths on each side
distPerYear = 96   #max distance per year for retreat or advance in metres
weights = "central"    # Central, Linear or equal

path = os.path.abspath('../')

if Input in imageInv:
    invert = 1
else:
    invert = 0

def getLandsatPath(path, GlacierName):
    landsatPath = pathjoin(path,'Data',GlacierName,'Landsat')
    return landsatPath

#Get bounding box from Glims database
def getBoundingBox(GlacierName):
    BoundingBox = querydb.findBoundingBoxByName(GlacierName)
    StartPoint =  querydb.findStartByName(GlacierName)
    return BoundingBox, StartPoint

def getPathVectors(path, GlacierName, DEMfile):
    BoundingBox, StartPoint = getBoundingBox(GlacierName)
    demfilepath = pathjoin(path,'Data',GlacierName,DEMfile)
    if not os.path.exists(demfilepath):
        demfilepath = pathjoin(path,'Data',GlacierName,DEMFILE1)
        if not os.path.exists(demfilepath):
            demfilepath = pathjoin(path,'Data',GlacierName,DEMFILE2)
            if not os.path.exists(demfilepath):
                raise FileNotFoundError("No DEM file")
    else:
        pass

    dim = Method1.getDimensions(demfilepath)
    start = Method1.beginningPoint(float(BoundingBox[0]),float(BoundingBox[1]),float(BoundingBox[2]),float(BoundingBox[3]),float(StartPoint[0]),float(StartPoint[1]),dim[0],dim[1],0.1)
    print(start)
    GLpath = Method1.findPath(pathjoin(path,'Data',GlacierName,DEMfile),int(start[1]),int(start[0]),flowline,DEMfile)
    pathVector = Method1.smoothPath(GLpath)
    pathVectors = Method1.parallelPath(pathVector,pathjoin(path,'Data',GlacierName,DEMfile),numParallel)
    return pathVectors

def downloadFiles(path,GlacierName):
    print("1.Querying Database for glacier bounds: "+GlacierName)
    try:
        BoundingBox, StartPoint = getBoundingBox(GlacierName)
    except Exception, e:
        print(str(e))
        pass

    try:
        print("2. Download Landsat")
        rgbplot.downloadLandsat(path,GlacierName,BoundingBox)
    except Exception, e:
        print(str(e))
        pass

    try:
        print("3.Download DEM from earth engine")
        bounds = ee_download.getBounds(float(BoundingBox[0]),float(BoundingBox[2]),float(BoundingBox[1]),float(BoundingBox[3]))
        DEMfile = ee_download.ee_download_DEM(path,GlacierName,bounds)
    except Exception, e:
        print(str(e))
        pass

    return BoundingBox, DEMfile

def makeRGBNDSI(path, GlacierName, BoundingBox):
    try:
        print("4. Classify Landsat and Save RGB and NDSI files")
        rgbplot.classifyLandsat(path,GlacierName,BoundingBox)
    except Exception, e:
        print(str(e))
        pass

def analyze(path, GlacierName, DEMfile):
    landsatPath = getLandsatPath(path, GlacierName)
    try:
        print("5.Determining the flowline of the glacier")
        pathVectors = getPathVectors(path, GlacierName, DEMfile)
    except Exception, e:
        print(str(e))
        pass

    try:
        print("6.Computing the Intensity profile Time Series")
        #TODO need to get a value for pmissing from somewhere
        #Hard-coded for now
        pmissing=.05
        timeline,IPTimeSeries, landsatFiles = Method3.intensityProfile(landsatPath,pathVectors,Input,pmissing,weights)
        timeline.sort()
        #Get the first value of the time series
        firsttime = IPTimeSeries[0].values()[0] 
        arcVector = Method3.arcLengthVector(firsttime,STEPSIZE,RESOLUTION)
    except Exception, e:
        print(str(e))
        pass

    try:
        print("7.Estimating Terminus and plot results")
        gm = querydb.findGroundMeasurement(GlacierName)
        grndmeas = {}
        list1 = []
        list2 = []
        for item in gm:
                list1.append(int(item[0]))
                list2.append(float(item[1]))
        grndmeas['year'] = list1
        grndmeas['gm'] = list2
        terminus = Method4.estimateTerminus(pathjoin(path,'Results',GlacierName,Input),GlacierName,arcVector,timeline,IPTimeSeries,grndmeas,invert,distPerYear)
    except Exception, e:
        print(str(e))
        pass

    return pathVectors, timeline, landsatFiles, terminus

def generatePlots(path, GlacierName, pathVectors, landsatFiles, timeline, terminus):
    landsatPath = getLandsatPath(path, GlacierName)
    try:
        print("8.Plotting flowline")
        folder = os.listdir(landsatPath)
        tifpath = pathjoin(landsatPath,folder[-1])
        if Input != 'B6_VCID_1':
                img = find('*.'+Input+'.tif',tifpath)
        else:
                img = find('*.B6.tif', tifpath)
        Method1.plotPaths(pathVectors,pathjoin(path,'Results',GlacierName,Input),GlacierName,img,numParallel,invert,Input,terminus[8],terminus[9])
        Method1.plotPathsDEM(pathVectors,pathjoin(path,'Results',GlacierName),GlacierName,pathjoin(path,'Results',GlacierName,DEMfile),numParallel,invert)
    except Exception, e:
        print(str(e))
        pass

    try:
        print("9.Generating terminus Plots")
        TI.terminusImages(pathVectors,landsatFiles,GlacierName,terminus,timeline,pathjoin(path,'Results',GlacierName,Input),invert,Input)
    except Exception, e:
        print(str(e))
        pass	

def processGlaciers(glaciers=GlacierNames, DEMfile=DEMFILE1):
    # Main loop over glaciers
    for GlacierName in GlacierNames:
        landsatPath = getLandsatPath(path,GlacierName)
        BoundingBox, DEMfile = downloadFiles(path, GlacierName)
        makeRGBNDSI(path, GlacierName, BoundingBox)
        pathVectors, timeline, landsatFiles, terminus = analyze(path, GlacierName, DEMfile)
        generatePlots(path, GlacierName, pathVectors, timeline, landsatFiles, terminus)

if __name__ == '__main__':
    processGlaciers(glaciers=GlacierNames)
