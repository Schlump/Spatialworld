FROM alpine:latest

ARG SEN2COR_VERSION='2.4.0'
ARG SEN2COR="Sen2Cor-${SEN2COR_VERSION}-Linux64.run"
ENV PATH="/opt/Sen2Cor-2.4.0-Linux64/bin:${PATH}"

RUN apk update && apk upgrade \
	&& apk add --no-cache --virtual .build-dependencies \
	wget \
	file \
	ca-certificates \
	&& mkdir -p /opt \
	&& cd /opt \
    && wget -q "http://step.esa.int/thirdparties/sen2cor/${SEN2COR_VERSION}/${SEN2COR}"  \
    && chmod +x ${SEN2COR} \
  	&& ./${SEN2COR} \
 	&& rm -rf ${SEN2COR} \
 	&& apk del .build-dependencies
