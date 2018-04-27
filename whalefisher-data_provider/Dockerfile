# Whalefisher Data-Provider

FROM python:3.5-alpine
LABEL maintainer="dream.paths.projekt@gmail.com"

# set working directory
RUN mkdir -p /usr/src/whalefisher
WORKDIR /usr/src/whalefisher

# add requirements (to leverage Docker cache)
ADD ./setup.py /usr/src/whalefisher/setup.py

# install requirements
# RUN sudo apt-get install python3.6-dev
RUN python setup.py install

# add app
ADD . /usr/src/whalefisher/

# run server
CMD ["python", "app.py"]

