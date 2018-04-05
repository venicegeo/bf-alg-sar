# Copyright 2018, RadiantBlue Technologies, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM debian:latest
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /work


RUN apt-get update; \
    apt-get install -y python-setuptools python-numpy python-dev libgdal-dev python-gdal swig git g++; \
    apt-get install -y libagg-dev libpotrace-dev; \
    easy_install pip; pip install wheel;

COPY requirements.txt /work/requirements.txt

RUN pip install cython;
RUN pip install -r requirements.txt
RUN pip install nose==1.3.7

RUN git clone https://github.com/venicegeo/bf-alg-sar
WORKDIR /work/bf-alg-sar
CMD /bin/bash
