import os
import numpy as np
import gdal
import glob

#root_folder = "/Users/luisevonpogrell/Desktop/Python/W5/"

#def Load_Raster (root_folder):
#    global rastername
#    rasternames = os.listdir(root_folder)
#    rasters = []
#    arrays = []
#    for rastername in rasternames:
#        raster.append(gdal.Open(rootfolder + rastername)) #("*.tif")
#        ds = gdal.Open(rootfolder + rastername)
#        arrays.append(np.array(ds.GetRasterBand(1).ReadAsArray()))
#    print(rastername)
#    return rasters, arrays

slope_ras = gdal.Open("/Users/luisevonpogrell/Desktop/Python/W5/SLOPE_Humboldt_sub.tif")
slope = slope_ras.GetRasterBand(1)
gt_slope = slope_ras.GetGeoTransform()

dem_ras = gdal.Open("/Users/luisevonpogrell/Desktop/Python/W5/DEM_Humboldt_sub.tif")
dem = dem_ras.GetRasterBand(1)
gt_dem = dem_ras.GetGeoTransform()

thp_ras = gdal.Open("/Users/luisevonpogrell/Desktop/Python/W5/THP_Humboldt_sub.tif")
thp = thp_ras.GetRasterBand(1)
gt_thp = thp_ras.GetGeoTransform()

path = "/Users/luisevonpogrell/Desktop/Python/W5/"

file_list = glob.glob(os.path.join(path, "*.tif"))

def rasteroverlap(file_list):
    UL_x_list = list()
    UL_y_list = list()
    LR_x_list = list()
    LR_y_list = list()
    for i in file_list:
        ds = gdal.Open(i)
        gt = ds.GetGeoTransform()
        UL_x, UL_y = gt[0], gt[3]
        LR_x = UL_x + (gt[1]*ds.RasterXSize)
        LR_y = UL_y + (gt[5]*ds.RasterYSize)
        UL_x_list.append(UL_x)
        UL_y_list.append(UL_y)
        LR_x_list.append(LR_x)
        LR_y_list.append(LR_y)
        print(os.path.basename(i), "UL_x:",UL_x, "UL_y:",UL_y, "LR_x:",LR_x, "LR_y:",LR_y)
    print('UL X:', max(UL_x_list),'UL Y:', min(UL_y_list))
    print('LR X:', min(LR_x_list),'LR Y:', max(LR_y_list))
    print("X range", (min(LR_x_list)- max(UL_x_list))/gt[1])
    print("Y range", (min(UL_y_list)- max(LR_y_list))/gt[1])

rasteroverlap(file_list)

# invert the geotransformation (from raster koordinates to "array" coordinates)
inv_gt_slope = gdal.InvGeoTransform(gt_slope)
print(inv_gt_slope)
offset_slope = gdal.ApplyGeoTransform(inv_gt_slope, 1399618.9749825108, 705060.6257949192)
xoff_slope, yoff_slope = map(int, offset_slope)
array_slope = slope.ReadAsArray(xoff_slope, yoff_slope, 599, 1239) #row, and column
print(array_slope)


inv_gt_dem = gdal.InvGeoTransform(gt_dem)
print(inv_gt_dem)
offset_dem = gdal.ApplyGeoTransform(inv_gt_dem, 1399618.9749825108, 705060.6257949192)
xoff_dem, yoff_dem = map(int, offset_dem)
array_dem = dem.ReadAsArray(xoff_dem, yoff_dem, 599, 1239) #row, and column
print(array_dem)
comp_dem = np.where(array_dem == 35536 , "NoData", array_dem)


inv_gt_thp = gdal.InvGeoTransform(gt_thp)
print(inv_gt_thp)
offset_thp = gdal.ApplyGeoTransform(inv_gt_thp, 1399618.9749825108, 705060.6257949192)
xoff_thp, yoff_thp = map(int, offset_thp)
array_thp = thp.ReadAsArray(xoff_thp, yoff_thp, 599, 1239) #row, and column
print(array_thp)
# calculate the common extend
# calculate dimensions of the array
# convert the three layers into arrays, get only the array values from the common extend
# get NoData values




# https://jakevdp.github.io/PythonDataScienceHandbook/