FROM postgres:9.6.5-alpine

ENV POSTGIS=2.3.2

RUN apk update \


	 && apk add --no-cache \
	 	ca-certificates \
	 	wget \
        autoconf \
        automake \
        g++ \
        json-c-dev \
        libtool \
        libxml2-dev \
        make 


RUN cd /tmp \

	&& echo "Installing PostGIS-${POSTGIS}..." \
	&& wget -q http://download.osgeo.org/postgis/source/postgis-${POSTGIS}.tar.gz\
	&& tar -zxf postgis-${POSTGIS}.tar.gz\
	&& cd postgis-${POSTGIS}\
	&& ./configure --with-geosconfig=/usr/bin/geos-config\
	&& make && make install