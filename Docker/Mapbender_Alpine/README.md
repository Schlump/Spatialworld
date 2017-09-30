## A docker recipe for Mapbender 3.0.6.3
### Based Nginx Docker image (Alpine:Latest) with PHP7
### With Supervisord

Image size of 281MB

### Install 
Download Dockerfile & nginx config file

cd into download directory 

docker build -t Mapbender .

### Run

docker run --name "Mapbender" -p 80:80 -d -t Mapbender
