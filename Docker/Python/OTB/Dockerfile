FROM debian:latest

ARG OTB_VERSION=6.2.0-rc1
ARG OTB_INSTALLVER=6.2.0
ARG OTB_DIR=/opt
ARG DEBIAN_FRONTEND=noninteractive
ARG DATA_VOL='/data'

ENV PYTHONPATH=$PYTHONPATH:${OTB_DIR}/OTB-${OTB_INSTALLVER}-Linux64/lib/python:/usr/bin/python
ENV PATH=$PATH:${OTB_DIR}/OTB-${OTB_INSTALLVER}-Linux64/bin

RUN apt-get update && apt-get install -y --no-install-recommends \
	python-pip \
	python2.7 \
	python-dev \
	wget \
	ca-certificates \
	file \
	&& pip install --upgrade pip \
	&& pip install numpy \
	&& mkdir -p ${OTB_DIR} \
	&& cd ${OTB_DIR} \
	&& wget -q https://www.orfeo-toolbox.org/packages/OTB-${OTB_VERSION}-Linux64.run \
	&& chmod +x OTB-${OTB_VERSION}-Linux64.run \
	&& ./OTB-${OTB_VERSION}-Linux64.run \
	&& rm -rf OTB-${OTB_VERSION}-Linux64.run \
	&& rm -rf /var/lib/apt/lists/* \
	&& mkdir -p ${DATA_VOL}


VOLUME [$DATA_VOL]


