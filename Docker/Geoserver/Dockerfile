FROM openjdk:8-jdk-alpine
LABEL maintainer="None"
LABEL version="0.1"
LABEL setup="Based openjdk-alpine"
LABEL description="Geoserver 2.11.2 built with GDAL 2.2.1 running on Jetty 9.4.6"

# Set JAVA_HOME to OpenJDK installation
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN addgroup -S jetty && adduser -D -S -H -G jetty jetty && rm -rf /etc/group- /etc/passwd- /etc/shadow-

ENV JETTY_HOME /usr/local/jetty
ENV PATH $JETTY_HOME/bin:$PATH
RUN mkdir -p "$JETTY_HOME"
WORKDIR $JETTY_HOME

ENV JETTY_VERSION 9.4.6.v20170531
ENV JETTY_TGZ_URL https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-home/$JETTY_VERSION/jetty-home-$JETTY_VERSION.tar.gz
ENV JETTY_BASE /var/lib/jetty

ENV GEOSERVER_VERSION=2.11.2
ENV GEOSERVER_DATA_DIR /var/lib/jetty/webapps/geoserver/data
ENV GDAL_VERSION=2.2.1

# GPG Keys are personal keys of Jetty committers (see https://github.com/eclipse/jetty.project/blob/0607c0e66e44b9c12a62b85551da3a0edce0281e/KEYS.txt)
ENV JETTY_GPG_KEYS \
	# Jan Bartel      <janb@mortbay.com>
	AED5EE6C45D0FE8D5D1B164F27DED4BF6216DB8F \
	# Jesse McConnell <jesse.mcconnell@gmail.com>
	2A684B57436A81FA8706B53C61C3351A438A3B7D \
	# Joakim Erdfelt  <joakim.erdfelt@gmail.com>
	5989BAF76217B843D66BE55B2D0E1FB8FE4B68B4 \
	# Joakim Erdfelt  <joakim@apache.org>
	B59B67FD7904984367F931800818D9D68FB67BAC \
	# Joakim Erdfelt  <joakim@erdfelt.com>
	BFBB21C246D7776836287A48A04E0C74ABB35FEA \
	# Simone Bordet   <simone.bordet@gmail.com>
	8B096546B1A8F02656B15D3B1677D141BCF3584D \
	# Greg Wilkins    <gregw@webtide.com>
	FBA2B18D238AB852DF95745C76157BDF03D0DCD6 \
	# Greg Wilkins    <gregw@webtide.com>
	5C9579B3DB2E506429319AAEF33B071B29559E1E

RUN set -xe 

	# Install required packages for build time. Will be removed when build finishes.
	# Update Alpine Linux, Install GDAL and wget for SSL transfer 
RUN apk update && apk upgrade 
RUN apk add --virtual .build-deps --no-cache\
	gnupg \
	#update-ca-certificates \
	ca-certificates \
	tar \
	g++ \
	libstdc++ \
	make \
	swig \
	apache-ant \
	linux-headers \
	curl \
	wget \

	&& curl -SL "$JETTY_TGZ_URL" -o jetty.tar.gz \
	&& curl -SL "$JETTY_TGZ_URL.asc" -o jetty.tar.gz.asc \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& for key in $JETTY_GPG_KEYS; do \
		gpg --keyserver  ipv4.pool.sks-keyservers.net --recv-keys "$key"; done \
	&& gpg --batch --verify jetty.tar.gz.asc jetty.tar.gz \
	&& rm -rf "$GNUPGHOME" \
	&& tar -xvzf jetty.tar.gz \
	&& mv jetty-home-$JETTY_VERSION/* ./ \
	&& sed -i '/jetty-logging/d' etc/jetty.conf \
	&& rm jetty.tar.gz* \
	&& rm -fr jetty-home-$JETTY_VERSION/ \



	# Download and install GeoServer
	&& mkdir -p $GEOSERVER_DATA_DIR \
	&& cd /var/lib/jetty/ \
	&& wget  -q http://sourceforge.net/projects/geoserver/files/GeoServer/${GEOSERVER_VERSION}/geoserver-${GEOSERVER_VERSION}-war.zip \
	&& unzip -q geoserver-${GEOSERVER_VERSION}-war.zip \
	&& mkdir -p webapps/geoserver/ \
	&& unzip -q geoserver.war -d webapps/geoserver/ \
	&& chown -R jetty:jetty /var/lib/jetty/ \
	&& rm geoserver-${GEOSERVER_VERSION}-war.zip \
	&& rm geoserver.war \

	# Compile GDAL
	&& wget -q http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz \
	&& mv gdal-${GDAL_VERSION}.tar.gz  /tmp/ \
	&& tar -zxf /tmp/gdal-${GDAL_VERSION}.tar.gz -C /tmp \
	&& cd /tmp/gdal-${GDAL_VERSION} && ./configure  --with-java=$JAVA_HOME && make -s && make install \

	# Install GDAL Java binding
	&& cd /tmp/gdal-${GDAL_VERSION}/swig/java\
	&& sed -i '/JAVA_HOME =/d' java.opt \
	&& make -s && make install \
	&& cp *.so /usr/local/lib/  \
	&& cp /tmp/gdal-${GDAL_VERSION}/swig/java/gdal.jar /var/lib/jetty/webapps/geoserver/WEB-INF/lib/ \
	&& mv /tmp/gdal-${GDAL_VERSION}/swig/java/gdal.jar /usr/share/gdal.jar \

	# Download and install Extensions
	&& wget -q https://sourceforge.net/projects/geoserver/files/GeoServer/${GEOSERVER_VERSION}/extensions/geoserver-${GEOSERVER_VERSION}-gdal-plugin.zip \
	&& wget -q https://sourceforge.net/projects/geoserver/files/GeoServer/${GEOSERVER_VERSION}/extensions/geoserver-${GEOSERVER_VERSION}-inspire-plugin.zip \
	&& unzip -oq geoserver-${GEOSERVER_VERSION}-gdal-plugin.zip -d /var/lib/jetty/webapps/geoserver/WEB-INF/lib/ \
	&& unzip -oq geoserver-${GEOSERVER_VERSION}-inspire-plugin.zip -d /var/lib/jetty/webapps/geoserver/WEB-INF/lib/ \
	&& rm geoserver-${GEOSERVER_VERSION}-gdal-plugin.zip \
	&& rm geoserver-${GEOSERVER_VERSION}-inspire-plugin.zip \


	&& wget -q http://download.java.net/media/jai/builds/release/1_1_3/jai-1_1_3-lib-linux-amd64.tar.gz \
	&& wget -q http://download.java.net/media/jai-imageio/builds/release/1.1/jai_imageio-1_1-lib-linux-amd64.tar.gz \
	&& tar -zxf jai-1_1_3-lib-linux-amd64.tar.gz -C /tmp \
	&& tar -zxf jai_imageio-1_1-lib-linux-amd64.tar.gz -C /tmp \
	&& mv /tmp/jai-1_1_3/lib/jai_codec.jar $JAVA_HOME/lib/ext  \
	&& mv /tmp/jai-1_1_3/lib/jai_core.jar $JAVA_HOME/lib/ext \
	&& mv /tmp/jai-1_1_3/lib/mlibwrapper_jai.jar $JAVA_HOME/lib/ext  \
	&& mv /tmp/jai-1_1_3/lib/*.so $JAVA_HOME/lib/amd64/  \
	&& mv /tmp/jai_imageio-1_1/lib/clibwrapper_jiio.jar $JAVA_HOME/lib/ext  \
	&& mv /tmp/jai_imageio-1_1/lib/jai_imageio.jar $JAVA_HOME/lib/ext  \
	&& mv /tmp/jai_imageio-1_1/lib/*.so $JAVA_HOME/lib/amd64 \


	# Remove installed packages and various cleanup
	&& apk del .build-deps \
	&& rm -rf /tmp/* \

	# Remove Geosever example data
	&& 	rm -rf $GEOSERVER_DATA_DIR/workspaces/*  \
	&&  rm -rf $GEOSERVER_DATA_DIR/coverages/*  \
	&&  rm -rf $GEOSERVER_DATA_DIR/layergroups/* \
	&&  rm -rf $GEOSERVER_DATA_DIR/data/* 



RUN mkdir -p "$JETTY_BASE"
WORKDIR $JETTY_BASE

RUN set -xe \
	&& java -jar "$JETTY_HOME/start.jar" --create-startd --add-to-start="server,http,deploy,jsp,jstl,ext,resources,websocket,setuid" \
	&& chown -R jetty:jetty "$JETTY_BASE" \
	&& rm -rf /tmp/hsperfdata_root

ENV TMPDIR /tmp/jetty
RUN set -xe \
	&& mkdir -p "$TMPDIR" \
	&& chown -R jetty:jetty "$TMPDIR"



ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/lib/jni:/usr/share/java:/usr/local/lib/



VOLUME $GEOSERVER_DATA_DIR	
EXPOSE 8080
CMD ["java","-jar","/usr/local/jetty/start.jar"]
