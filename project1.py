import gdal
import glob
import os

path = '/Users/luisevonpogrell/Desktop/Python/Assignment02_data/'

file_list = glob.glob(os.path.join(path, "*.tif"))

for i in file_list:
    ds = gdal.Open(i)
    gt = ds.GetGeoTransform()
    UL_x, UL_y = gt[0], gt[3]
    LR_x = UL_x + (gt[1]*ds.RasterXSize)
    LR_y = UL_y + (gt[5]*ds.RasterYSize)
    print(UL_x, UL_y, LR_x, LR_y)