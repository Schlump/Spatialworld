FROM continuumio/miniconda:latest

ARG SEN2THREE_VERSION='1.1.0'

RUN apt-get update && apt-get install -y --no-install-recommends \
	wget \
	ca-certificates \
	&& cd /tmp \
	&& mkdir -p /data \
	&& wget -q "http://step.esa.int/thirdparties/sen2three/${SEN2THREE_VERSION}/sen2three-${SEN2THREE_VERSION}.tar.gz" \
	&& tar -zxf sen2three-${SEN2THREE_VERSION}.tar.gz \
	&& cd sen2three-${SEN2THREE_VERSION} \
	&& /bin/echo -e "y\ny\ny\n" | python setup.py install \
	&& conda install --yes pytables scipy pillow matplotlib \
	&& rm -rf /tmp/* \
	&& rm -rf /var/lib/apt/lists/* \
	&& conda clean --all

VOLUME [ "/data" ]
