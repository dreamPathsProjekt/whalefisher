# Whalefisher Data-Provider

FROM python:3.5-alpine
LABEL maintainer="dream.paths.projekt@gmail.com"

# set working directory
RUN mkdir -p /usr/src/whalefisher
WORKDIR /usr/src/whalefisher

RUN apk add --no-cache python3-dev libevent-dev gcc musl-dev linux-headers libc-dev
# add requirements (to leverage Docker cache)
ADD ./setup.py /usr/src/whalefisher/setup.py

# install requirements
# RUN sudo apt-get install python3.6-dev
RUN python setup.py install && \
    pip install gunicorn

# add app
ADD . /usr/src/whalefisher/

# run server
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "wsgi"]

