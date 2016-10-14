import os
import sys
import numpy as np
import json
import bf-Sar2Shoreline
from beachfront.vectorize import trace_it

try:
    import gdal
    import osr
except:
    from osgeo import gdal, osr

def main(img_path, out_path, kernelSize=kernelSize, scaleFactor=sf):
    #run bf-Sar2Shoreline --> returns binary mask
    binary_mask = bf-Sar2Shoreline.WaterExtractionSAR(img_path, kernelSize=kernelSize, scaleFactor=sf)
    #run vectorizing code from bf-py --> returns vector
    coastline = beachfront.vectorize.trace_it(binary)
    # write to file
    with open('_', 'w') as outfile:
        json.dump(coastline, outfile)

def usage():
    print("""
          Usage:
          bf-algo-sar -i in_raster -o out_raster
          -k kernel_Size (optional, default=10)
          -s ScaleFactor (optional, default=0.1)"""
          )
    sys.exit(1)


if __name__ == '__main__':

    img_path = None
    out_path = None
    kernelSize = 10
    sf = 0.1

    for i in range(len(sys.argv)-1):
        arg = sys.argv[i]
        if arg == '-i':
            img_path = sys.argv[i+1]
        elif arg == '-o':
            out_path = sys.argv[i+1]
        elif arg == '-k':
            kernelSize = int(sys.argv[i+1])
        elif arg == '-s':
            sf = float(sys.argv[i+1])

    if img_path is None:
        usage()
    if out_path is None:
        usage()

    main(img_path, out_path, kernelSize=kernelSize, scaleFactor=sf)
    sys.exit(0)
