import os
import sys
import numpy as np
import json
import bf_Sar2Shoreline
from gippy import GeoImage
from bf.beachfront import vectorize

try:
    import gdal
    import osr
except:
    from osgeo import gdal, osr

def main(img_path, out_path, kernelSize=10, scaleFactor=0.1, cleanup=1):
    #run bf-Sar2Shoreline --> returns binary mask
    name = bf_Sar2Shoreline.xO_names(out_path)
    binary_mask ='%s/%s_binary.tif' % (name['directory'],
                                  name['basename'])
    status = bf_Sar2Shoreline.WaterExtractionSAR(img_path,
                                                 out_path=binary_mask,
                                                 kernelSize=kernelSize,
                                                 scaleFactor=scaleFactor)
    geoimg = GeoImage(binary_mask)
    geoimg.set_nodata(3)
    #run vectorizing code from bf-py --> returns vector
    lines = vectorize.potrace(geoimg, turdsize=1.0, tolerance=0.1)
    vectorize.save_geojson(lines, out_path, source='SAR imagery')
    geoimg = None
    if cleanup == 1:
        os.remove(binary_mask)

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
    cleanup = 0

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
        elif arg == '-c':
            cleanup == int(sys.argv[i+1])

    if img_path is None:
        usage()
    if out_path is None:
        usage()

    main(img_path, out_path, kernelSize=kernelSize, scaleFactor=sf, cleanup=cleanup)
    sys.exit(0)
