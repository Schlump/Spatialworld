## A docker recipe for Geoserver 2.11.2 built with GDAL 2.2.1 running on Jetty 9.4.6
### Based openjdk:8-jdk-alpine

Image size of 449MB

### Install 
Download Dockerfile 

cd into download directory 

docker build -t Geoserver .

### Run

docker run --name "geoserver" -p 8080:8080 -d -t Geoserver