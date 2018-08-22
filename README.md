# bf-alg-sar
The bf-alg-sar project is an implementation of the SAR (Synthetic Aperture Radar) shoreline detection algorithm written by the Beachfront team, with simple texture and size-based processing for SAR (Synthetic Aperture Radar) waterline extraction. It has been designed and tested using European Space Agency's Sentinel-1 SAR GRD products. For best results, it is recommended to use mixed-polarization VH (vertical transmit and horizontal receive) data. This is a simple algorithm looking for spatially large, homogeneous, low-amplitude returns. If using input data with a higher resolution, it may be necessary to modify the scale factor and kernel size.

## Usage:
To run bf-alg-sar, use the following command-line template:

	$ bf-algo-sar -i in_raster -o out_raster -k kernel_Size (optional, default=10) -s ScaleFactor (optional, default=0.1)

