from main import *

def partial():
    GlacierName = GlacierNames[0]
    landsatPath = pathjoin(path,'Data',GlacierName,'Landsat')
    DEMfile=DEMFILE2
    pathVectors, timeline, landsatFiles, terminus = analyze(path, GlacierName, DEMfile)


if __name__ == '__main__':
    partial()
