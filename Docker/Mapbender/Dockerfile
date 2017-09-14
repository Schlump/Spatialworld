FROM nginx
ENV MAPBENDER=3.0.6.3
ENV MAPDIR='/var/www/mapbender'

RUN apt-get update && apt-get install -y --no-install-recommends \
	wget \
	php \
	php-xml \
	php-mbstring \
	php-mysql \
	php-bz2 \
	php-curl \
	php-gd \
	php-intl \
	php-mcrypt \
	php-memcache \
	php-sqlite3 \
	php-pgsql \
	sqlite3 \
	php-fpm 

COPY nginx.conf /etc/nginx/conf.d/default.conf 

RUN mkdir -p ${MAPDIR} \
	&& cd /tmp \
	&& wget -q http://mapbender3.org/builds/mapbender3-starter-${MAPBENDER}.tar.gz \
	&& tar -zxf mapbender3-starter-${MAPBENDER}.tar.gz \
	&& mv /tmp/mapbender3-starter-${MAPBENDER}/* ${MAPDIR}/  \
	&& rm -rf /tmp/* \
	&& rm -rf ${MAPDIR}/app/cache/* ${MAPDIR}/app/logs/* \
	&& chown -R www-data:www-data ${MAPDIR} \
	&& chmod -R ugo+r ${MAPDIR} \
	&& chmod -R ug+w ${MAPDIR}/web \
	&& sed -e 's/;daemonize = yes/daemonize = no/' -i /etc/php/7.0/fpm/php-fpm.conf \
	&& sed -e 's/;listen\.owner/listen.owner/' -i /etc/php/7.0/fpm/pool.d/www.conf \
	&& sed -e 's/;listen\.group/listen.group/' -i /etc/php/7.0/fpm/pool.d/www.conf \
	&& sed -e 's/listen = .run.php.php7.0-fpm.sock/listen = 127.0.0.1:9000/' -i /etc/php/7.0/fpm/pool.d/www.conf \
	&& sed -e 's/;catch_workers_output/catch_workers_output/' -i /etc/php/7.0/fpm/pool.d/www.conf \
	&& sed -i "s@/mapbender@$MAPDIR@" /etc/nginx/conf.d/default.conf

RUN service php7.0-fpm start
CMD /etc/init.d/php7.0-fpm restart; nginx -g 'daemon off;'



