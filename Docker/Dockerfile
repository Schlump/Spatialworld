
FROM debian:latest

ARG SEN2COR_VERSION='2.4.0'
ARG SEN2COR="Sen2Cor-${SEN2COR_VERSION}-Linux64.run"
ARG DIR='/opt/'

RUN DEBIAN_FRONTEND=noninteractive apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    wget \
    file \
    ca-certificates \
    && cd ${DIR} \
    && wget -q "http://step.esa.int/thirdparties/sen2cor/${SEN2COR_VERSION}/${SEN2COR}"  \
    && chmod +x ${SEN2COR} \
  	&& ./${SEN2COR} \
 	&& rm -rf ${SEN2COR} 


#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
ENTRYPOINT ["/bin/bash"]




