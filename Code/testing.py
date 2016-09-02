from main import *

def partial():
    GlacierName = GlacierNames[0]
    landsatPath = pathjoin(path,'Data',GlacierName,'Landsat')
    DEMfile=DEMFILE2
    pathVectors, timeline, landsatFiles, terminus = analyze(path, GlacierName, DEMfile)
    print("pathVectors")
    print(pathVectors)
    print("timeline")
    print(timeline)
    print("terminus")
    print(terminus)


    print("Generating Plots")
    generatePlots(path, GlacierName, pathVectors, timeline, terminus)

if __name__ == '__main__':
    partial()
