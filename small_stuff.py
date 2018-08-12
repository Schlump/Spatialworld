#!/usr/bin/python

def df2geodf(df):
    from shapely.geometry import Point
    import geopandas as gp
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    crs = None
    geo_df = gp.GeoDataFrame(df, crs=crs, geometry=geometry)
    geo_df.crs = {'init' :'epsg:31468'}

    return geo_df



# calculate nearest neighbor based on cKDTree and return distance
def NN(df):
    from scipy.spatial import cKDTree
    tree = cKDTree(list(zip(df.x,df.y)))
    points = list(zip(df.x,df.y))
    distances, indices = tree.query(points, k=2)

    return pd.DataFrame(distances).ix[:,1]




def getcsvlengths(file):
    import subprocess
    import re
    string = re.findall('\d+',str(subprocess.check_output(["wc -l "+file],shell=True)))

    return string
