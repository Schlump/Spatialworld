FROM nginx:alpine
ENV MAPBENDER=3.0.6.3
ENV MAPDIR='/var/www/mapbender'
ENV USER=nginx
RUN apk update && apk upgrade 
RUN apk add --no-cache \
	supervisor \
	curl \
	php7 \
	php7-mbstring \
	php7-bz2 \
	php7-openssl \
	php7-curl \
	php7-gd \
	php7-intl \
	php7-xml \
	php7-session \
	php7-mcrypt \
	php7-sqlite3 \
	php7-pdo \
	php7-pdo_sqlite \
	php7-pgsql \
	php7-ctype \
	php7-json \
	php7-xml \
	php7-dom \
	php7-fpm 

COPY nginx.conf /etc/nginx/conf.d/default.conf 
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p ${MAPDIR} \
	&& cd /tmp \
	&& curl -s http://mapbender3.org/builds/mapbender3-starter-${MAPBENDER}.tar.gz > mapbender3-starter-${MAPBENDER}.tar.gz \
	&& tar -zxf mapbender3-starter-${MAPBENDER}.tar.gz \
	&& mv /tmp/mapbender3-starter-${MAPBENDER}/* ${MAPDIR}/  \
	&& rm -rf /tmp/* \
	&& rm -rf ${MAPDIR}/app/cache/* ${MAPDIR}/app/logs/* \
	&& mkdir -p ${MAPDIR}/app/cache/prod \
	&& chown -R ${USER}:${USER} ${MAPDIR} \
	&& chmod -R ugo+r ${MAPDIR} \
	&& chmod -R ug+w ${MAPDIR}/web \
	&& chmod -R 0777 ${MAPDIR}/app/cache/ \
	&& chmod -R 0777 ${MAPDIR}/app/logs/ \
	&& sed -e 's/;daemonize = yes/daemonize = no/' -i /etc/php7/php-fpm.conf \
	&& sed -e 's/;listen\.owner/listen.owner/' -i /etc/php7/php-fpm.d/www.conf \
	&& sed -e 's/;listen\.group/listen.group/' -i /etc/php7/php-fpm.d/www.conf \
	&& sed -e 's/listen = .run.php.php7.0-fpm.sock/listen = 127.0.0.1:9000/' -i /etc/php7/php-fpm.d/www.conf \
	&& sed -e 's/;catch_workers_output/catch_workers_output/' -i /etc/php7/php-fpm.d/www.conf \
	&& sed -i "s@/mapbender@$MAPDIR/web@" /etc/nginx/conf.d/default.conf \
	&& mkdir /run/php 

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]






