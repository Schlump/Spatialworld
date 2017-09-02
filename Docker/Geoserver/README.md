## A docker recipe for GeoServer for Geoserver 2.11.2 built with GDAL 2.2.1 running on Jetty 9.4.6
### Based openjdk:8-jdk-alpine

### Install 
git clone git://github.com/schlump/Docker/Geoserver

docker build -t schlump/Geoserver .

### Run

docker run --name "geoserver" -p 8080:8080 -d -t schlump/Geoserver
