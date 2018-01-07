import os
import re
import xarray as xr
import scipy.ndimage
import numpy as np

def read_sentinel_dir(dir_):
    id_ = os.listdir(dir_+'/GRANULE')[0]
    imgdir = dir_+'/GRANULE/{}/IMG_DATA/'.format(id_)
    tileREXP = re.compile(r'.*(%s).*B(01|02|03|04|05|06|07|08|8A|09|10|11|12).jp2$' %id_.split('_')[1])
    tile = [xr.open_rasterio(imgdir+file) for file in sorted(os.listdir(imgdir)) if re.match(tileREXP,file)]
    return tile


def resample_and_merge(list_of_arrays):
    i = 0
    bandnumbers = {
        1: 'Band 2',
        0:'Band 1',
        2: 'Band 3',
        3: 'Band 4',
        4: 'Band 5',
        5: 'Band 6',
        6: 'Band 7',
        7: 'Band 8',
        12: 'Band 8A',
        8: 'Band 9',
        9: 'Band 10',
        10: 'Band 11',
        11: 'Band 12'        
    }

    for key, value in bandnumbers.items():
        coords = get_coordinates(list_of_arrays)
        if value == 'Band 2':
            ds = list_of_arrays[key].to_dataset(name=str(value))
            
        res = list_of_arrays[key].attrs['res'][0]
        if  res != 10:
            print ('Resampling {} to {}m'.format(value,10))
            values = np.kron(list_of_arrays[key].values / int(res/10), np.ones((int(res/10),int(res/10))))
            #values = scipy.ndimage.zoom(list_of_arrays[key].values, int(res/10), mode='nearest')
            array = xr.DataArray(values,coords=coords,dims=['band','x','y'])
            ds[str(value)] = array
        else:
            ds[str(value)] = list_of_arrays[key]
            
    return ds
            
def get_coordinates(list_of_arrays):
    for band in list_of_arrays:
        if band.attrs['res'][0] == 10:
            coords=band.coords
            break
        else:
            continue
    
    return coords
