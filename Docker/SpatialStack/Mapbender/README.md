## A docker recipe for Mapbender 3.0.6.3
### Based Nginx Docker image (Debian:Stretch) with PHP7
### With Supervisord

Image size of 399MB

### Install 
Download Dockerfile & config files

cd into download directory 

docker build -t Mapbender .

### Run

docker run --name "Mapbender" -p 80:80 -d -t Mapbender
