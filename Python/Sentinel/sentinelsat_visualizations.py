import requests
import folium
import geopandas as gpd 
import pandas as pd 
from PIL import Image
import io
import matplotlib.pyplot as plt
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date





def show_quicklook(id_,username,password):
    url = "https://scihub.copernicus.eu/apihub/odata/v1/Products('{}')/Products('Quicklook')/$value".format(id_)
    bytes_img = requests.session().get(url, auth=(username,password)).content
    return Image.open(io.BytesIO(bytes_img))



def plot_footprint_folium(GeoDataFrame):

    map_ = folium.Map(location=[gdf.centroid.geometry.y[0],gdf.centroid.geometry.x[0]],
                    zoom_start=5)
    folium.GeoJson(GeoDataFrame['geometry']).add_to(map_)
    for i, row in gdf.iterrows():
        string = '<i>'+str(row['tileid'])+'<i>'
        folium.Marker(location=([row['geometry'].centroid.y, row['geometry'].centroid.x]
                 ),popup=string).add_to(map_)
                      


    return map_
