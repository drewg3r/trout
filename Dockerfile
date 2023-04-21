FROM python:3.11-buster

ENV DATA_DIR=/data
ENV MEDIA_DIR=$DATA_DIR/media
ENV STATIC_ROOT=$DATA_DIR/static

RUN adduser --system --uid 141 uwsgi && \
    apt-get update && \
    apt-get install -y gettext && \
    pip install --upgrade pip && \
    pip install 'uwsgi~=2.0.20' && \
    mkdir -p $MEDIA_DIR $STATIC_ROOT && \
    chown -R 141.141 $DATA_DIR

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY --chown=141 src/ /src
COPY --chown=141 uwsgi.ini /

COPY resources/ /usr/bin

WORKDIR /src
USER uwsgi

CMD ["run.sh"]
