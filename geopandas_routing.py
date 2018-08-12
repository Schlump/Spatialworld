#!/usr/bin/python
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

def route(df, latS, longS, latE, longE, service='route', profile='driving'):
    """
    Routes from Start to endpoint using OpenSourceRoutingMachine.
    Parameters
    ----------
    latS: string
        Name of column with latitude coordinates for start point
    longS: string
        Name of column with longitude coordinates for start point
    latE: string
        Name of column with latitude coordinates for end point
    longE: string
        Name of column with longitude coordinates for end point
    service : string
        One of the following values:  route ,  nearest ,  table ,  match ,  trip
    profile : string
        Mode of transportation: driving, car?!, foot, bike
    Returns
    -------
    GeoDataFrame
    """
    geometries = []
    durations = []
    distances = []
    coordinates = []

    for index, row in df.iterrows():
        lat1 = row[latS]
        long1 = row[longS]
        lat2 = row[latE]
        long2 = row[longE]

        if (lat1 and long1) == 0 or (lat2 and long2) == 0:
            geometry, distance, duration = np.nan, np.nan, np.nan

        else:
            max_tries = 10
            for attempt in range(max_tries):
                try:
                    url = 'http://router.project-osrm.org/' + service + '/v1/' + profile + '/'
                    params = str(long1) + ',' + str(lat1) + ';' + str(long2) + ',' + str(
                        lat2) + '?geometries=geojson&overview=full'
                    r = requests.get(url + params)
                    r.raise_for_status()
                    rjson = r.json()
                    geometry = LineString(rjson['routes'][0]['geometry']['coordinates'])
                    distance = rjson['routes'][0]['distance']
                    duration = rjson['routes'][0]['duration']

                except requests.exceptions.HTTPError as err:
                    if attempt == max_tries - 1:
                        geometry, distance, duration = np.nan, np.nan, np.nan
                        print (err)

        geometries.append(str(geometry))
        durations.append(distance)
        distances.append(duration)
        coordinates.append([lat1, long1, lat2, long2])

    result = gpd.GeoDataFrame([distances, durations, geometries, coordinates]).transpose()
    result.columns = ['distance', 'duration', 'geometry', 'coordinates']
    result[['distance', 'duration']] = result[['distance', 'duration']].astype(float)

    return result
