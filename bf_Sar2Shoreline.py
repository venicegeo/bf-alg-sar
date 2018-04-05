import os
import sys
import numpy as np
import scipy
from scipy import ndimage
try:
    from skimage.filter import threshold_otsu
else:
    from skimage.filters import threshold_otsu
try:
    import gdal
    import osr
except:
    from osgeo import gdal, osr


def WaterExtractionSAR(img_path, out_path=None, kernelSize=10, scaleFactor=None):
    if scaleFactor is not None:
        img_path = rescaleImage(img_path, out_path=None, scaleFactor=scaleFactor)
    #img = readImage(img_path)
    rs = gdal.Open(img_path)
    rb = rs.GetRasterBand(1)
    img = rb.ReadAsArray()
    noDataValue = rb.GetNoDataValue()
    if noDataValue is not None:
        noData_mask = (img == noDataValue)
    rb = None
    rs = None
    img = scipy.ndimage.filters.median_filter(img, size=(kernelSize))
    thresh = threshold_otsu(img)
    img = img > thresh
    img = img.astype('uint8')
    img = scipy.ndimage.filters.median_filter(img, size=(kernelSize))
    if noDataValue is not None:
        img[noData_mask] = 3
    if out_path is not None:
        saveArrayAsRaster(img_path, out_path, img)
        rs = gdal.Open(out_path, gdal.GA_Update)
        rb = rs.GetRasterBand(1)
        colortable = gdal.ColorTable()
        colortable.SetColorEntry(0,(50, 200, 255))
        colortable.SetColorEntry(1,(187, 128, 25))
        colortable.SetColorEntry(3,(0, 0, 0))
        rb.SetColorTable(colortable)
        rb.FlushCache()
        rs.FlushCache()
        rs = None
        if scaleFactor is not None:
            os.remove(img_path)
        return 0
    else:
        if scaleFactor is not None:
            os.remove(img_path)
        return img


def rescaleImage(img_path,out_path=None,scaleFactor=0.10, epsg=3857):
    rs = gdal.Open(img_path)
    x0 = rs.RasterXSize
    y0 = rs.RasterYSize
    x1 = x0 * scaleFactor
    y1 = y0 * scaleFactor
    rs = None
    if out_path is None:
        name = xO_names(img_path)
        out_path = '%s/%s_rs.%s' % (name['directory'], name['basename'], name['extension'])
    exeString = 'gdalwarp -ts %s %s -t_srs EPSG:%s %s %s' % (x1, y1, epsg, img_path, out_path)
    status = os.system(exeString)
    return out_path


def readImage(imgPath):
    i1_src = gdal.Open(imgPath)
    i1 = i1_src.ReadAsArray()
    if i1.ndim > 2:
        i1 = np.rollaxis(i1, 0, 3)
    return i1


def saveArrayAsRaster(rasterfn, newRasterfn, array):
    raster = gdal.Open(rasterfn)
    # nBands = raster.count
    checksum = array.ndim
    if checksum == 3:
        temp = array.shape
        nBands = temp[2]
    else:
        nBands = 1
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    if array.dtype == 'uint8':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Byte)
    elif array.dtype == 'int16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Int16)
    elif array.dtype == 'float16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Float32)
    elif array.dtype == 'float32':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Float32)
    elif array.dtype == 'int32':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_Int32)
    elif array.dtype == 'uint16':
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_UInt16)
    else:
        outRaster = driver.Create(newRasterfn, cols, rows, nBands,
                                  gdal.GDT_CFloat64)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0,
                               pixelHeight))
    if nBands > 1:
        for i in range(1, (nBands + 1)):
            outband = outRaster.GetRasterBand(i)
            x = i-1
            outband.WriteArray(array[:, :, x])
    else:
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


def xO_names(path):
    baseWExt = os.path.basename(path)
    temp = baseWExt.split('.')
    basename = temp[0]
    if len(temp) == 2:
        extension = temp[1]
    else:
        extension = ''
    folder = os.path.dirname(path)
    if folder == '/':
        folder = ''
    outName = {'basename': basename, 'extension': extension,
               'directory': folder}
    return outName


def usage():
    print("""
          Usage:
          bf-Sar2Shoreline -i in_raster -o out_raster
          -k kernel_Size (optional)
          -s ScaleFactor (optional)"""
          )
    sys.exit(1)


if __name__ == '__main__':

    img_path = None
    out_path = None
    kernelSize = 10
    sf = None

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

    WaterExtractionSAR(img_path, out_path=out_path, kernelSize=kernelSize, scaleFactor=sf)
    sys.exit(0)
