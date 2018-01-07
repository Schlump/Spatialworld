import requests
import folium
import geopandas as gpd 
import pandas as pd 
from PIL import Image
import io
import matplotlib.pyplot as plt
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import re




def show_quicklook(id_,username,password):
    data = "https://scihub.copernicus.eu/apihub/odata/v1/Products('{}')/Attributes('Sensing%20start')".format(id_)
    data = requests.session().get(data, auth=(username,password)).text
    sensingtime = re.search(r'<d:Value[^>]*>([^<]+)</d:Value>',data).group(0)
    sensingtime = sensingtime.replace('<d:Value>','').replace('</d:Value>','')
    quicklook = "https://scihub.copernicus.eu/apihub/odata/v1/Products('{}')/Products('Quicklook')/$value".format(id_)
    bytes_img = requests.session().get(quicklook, auth=(username,password)).content
    img = Image.open(io.BytesIO(bytes_img))
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_xticks([])
    ax.set_yticks([])
    plt.title(id_, fontsize=16)
    plt.xlabel(sensingtime,fontsize=16)
    plt.imshow(img)


def plot_footprint_folium(GeoDataFrame):

    map_ = folium.Map(location=[gdf.centroid.geometry.y[0],gdf.centroid.geometry.x[0]],
                    zoom_start=5)
    folium.GeoJson(GeoDataFrame['geometry']).add_to(map_)
    for i, row in gdf.iterrows():
        string = '<i>'+str(row['tileid'])+'<i>'
        folium.Marker(location=([row['geometry'].centroid.y, row['geometry'].centroid.x]
                 ),popup=string).add_to(map_)
                      
    return map_




def downlod_quicklook(id_,username,password):
	url = "https://scihub.copernicus.eu/apihub/odata/v1/Products('{}')/Products('Quicklook')/$value".format(id_)
    bytes_img = requests.session().get(url, auth=(username,password)).content
    if type(bytes_img) != bytes:
    	break
	write_image = open(id_+'_quicklook.jpg', 'wb') 
	write_image.write(bytes_img) 
	write_image.close()