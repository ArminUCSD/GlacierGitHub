import os
import rpy2.robjects as robjects
import rpy2.rinterface as ri
from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects.conversion import py2ri
import numpy
robjects.numpy2ri.activate()

def estimateTerminus(path,glacier,arcVector,timeline,ipTimeSeries,gm,invert,distPerYear, ip):

	ri.initr()
	robjects.r('''source('terminus.R')''')
	r_tp = robjects.globalenv['terminus']
	obs = robjects.DataFrame(ipTimeSeries)
	arcV = robjects.IntVector(arcVector)
	timlin = robjects.FloatVector(timeline)
	if gm :
		gmeas={}
		gmeas['v1'] = robjects.IntVector(gm['year'])
		gmeas['v2'] = robjects.FloatVector(gm['gm'])
		grndmeas = robjects.DataFrame(gmeas)
	else:
		grndmeas = robjects.r("NULL")
	direc = path
	if not os.path.exists(direc): os.makedirs(direc)
	terminus = r_tp(glacier = glacier, obs = obs, ss = arcV, tt = timlin, meas = grndmeas, plot=ri.TRUE, direc = direc, linefit = 0,
		temporal = 2, invert = invert, distPerYear = distPerYear, IP = ip)
	return terminus
