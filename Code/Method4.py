import os
import rpy2.robjects as robjects
import rpy2.rinterface as ri
from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects.conversion import py2ri
from rpy2.robjects.vectors import FloatVector
import numpy
from terminus_est import terminus_paths
robjects.numpy2ri.activate()

def getIPDict(ipTimeSeries):
    ipdict = {}
    for d in ipTimeSeries:
        ipdict.update(d)
        return ipdict

def estimateTerminus(path,glacier,arcVector,timeline,ipTimeSeries,gm,invert,distPerYear):

	ri.initr()
	robjects.r('''source('terminus.R')''')
	r_tp = robjects.globalenv['terminus']
        r_sm = robjects.globalenv['spatial_smooth']

        print("ipTimeSeries")
        print(ipTimeSeries)

        ipdict = getIPDict(ipTimeSeries)
        print("ipdict")
        print(ipdict)
	obs = robjects.DataFrame(ipdict)
        print("OBS")
        print(obs)

	arcV = robjects.IntVector(arcVector)
	timlin = robjects.FloatVector(timeline)

        #TODO Why is knotS passed as a variable?
        knotS = min( round(len(arcV)/4)+4, 35+4)
        smoothItem = r_sm(obs=obs, ss=arcV, knotS=knotS)
        print('smoothItem')
        print(smoothItem)

        #smoothItem[0] = sSmooth$dd1 = first derivative
        theta0 = terminus_paths(smoothItem[0],timlin,arcV,glacier,invert,distPerYear)
	if gm :
		gmeas={}
		gmeas['v1'] = robjects.IntVector(gm['year'])
		gmeas['v2'] = robjects.FloatVector(gm['gm'])
		grndmeas = robjects.DataFrame(gmeas)
	else:
		grndmeas = robjects.r("NULL")
	direc = path
	if not os.path.exists(direc): os.makedirs(direc)
        print('======')
        print('theta0')
        print(theta0)
        print("-----")
        print("arcV")
        print(arcV)
        print("-----")
        print("arcV[theta0]")
        print(arcV[theta0])
        print("-----")
        print("len(timlin)")
        print(len(timlin))
	terminus = r_tp(glacier = glacier, obs = obs, ss = arcV, tt = timlin, sSmooth=smoothItem, theta0=theta0, meas = grndmeas, plot=ri.TRUE, direc = direc, linefit = 0,
		temporal = 0, invert = invert, distPerYear = distPerYear)
	return terminus
