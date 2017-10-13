FROM postgres:9.6.5
MAINTAINER None
ENV POSTGRES_VERSION=9.6
ENV POSTGIS_VERSION=2.3

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-${POSTGRES_VERSION}-postgis-${POSTGIS_VERSION} \
           postgresql-${POSTGRES_VERSION}-postgis-${POSTGIS_VERSION}-scripts \
           postgresql-${POSTGRES_VERSION}-pgrouting \
      && rm -rf /var/lib/apt/lists/* \
      && mkdir -p /docker-entrypoint-initdb.d

COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
