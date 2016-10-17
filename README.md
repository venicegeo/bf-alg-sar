# bf-alg-sar
Simple texture and size-based processing for SAR to extract waterline
Designed and tested using European Space Agency's Sentinel-1 SAR GRD products.  For best results use mixed-polarization VH data.
This is a simple algorithm looking for spatially large, homogenous, low-amplitude returns.  If using input data with a higher resolution, it may be necessary to modify the scale factor and kernel size.

Usage:
          bf-algo-sar -i in_raster -o out_raster
          -k kernel_Size (optional, default=10)
          -s ScaleFactor (optional, default=0.1)
