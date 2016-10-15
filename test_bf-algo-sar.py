import os
try:
    import gdal
    import osr
except:
    from osgeo import gdal, osr

import bf_Sar2Shoreline
import bf_algo_sar


# have sample input sar image
# have sample binary mask output
# have sample geojson results
# test if these all compare

def test_bf_Sar2Shoreline():
    """test binary mask generation"""
    img1 = bf_Sar2Shoreline.WaterExtractionSAR('testdata/tile41.tif', kernelSize=10, scaleFactor=0.10)
    rs2 = gdal.Open('testdata/binary_groundtruth.tif')
    img2 = rs2.ReadAsArray()
    assert img1.mean() == img2.mean()


def test_rescale():
    """test image rescaling"""
    bf_Sar2Shoreline.rescaleImage('testdata/tile41.tif',out_path='testdata/tile41_rs.tif',scaleFactor=0.10, epsg=4326)
    rs = gdal.Open('testdata/tile41_rs.tif')
    img1 = rs.ReadAsArray()
    rs2 = gdal.Open('testdata/resample_groundtruth.tif')
    img2 = rs2.ReadAsArray()
    os.remove('testdata/tile41_rs.tif')
    assert img1.mean() == img2.mean()


def test_bf_algo_sar():
    """test geojson string generation"""
    bf_algo_sar.main('testdata/tile41.tif',
                     'testdata/tile41_results.geojson',
                     kernelSize=10,
                     scaleFactor=0.10)
    f1 = open('testdata/tile41_results.geojson')
    results = f1.readlines()
    f2 = open('testdata/groundtruth.geojson')
    gtruth = f2.readlines()
    assert results == gtruth
