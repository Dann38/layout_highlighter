ARG REPOSITORY="docker.io"
FROM ubuntu:22.04

WORKDIR /imgDoc

COPY ./requirements.txt /imgDoc/requirements.txt

# install python3
RUN apt-get update && apt-get install -y python3 python3-pip software-properties-common ffmpeg libsm6 libxext6

# install tesseract
RUN add-apt-repository -y  ppa:alex-p/tesseract-ocr-devel && apt update --allow-releaseinfo-change && apt install -y tesseract-ocr tesseract-ocr-rus


RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /imgDoc/requirements.txt
RUN python3 -m pip install setuptools-scm && pip install --upgrade setuptools
#

# VOLUME /build

COPY . /build/
COPY ./model_training/models /build/models

WORKDIR /build
RUN python3 -m pip install .

WORKDIR /build
ENV HOME=/build/

CMD ["python3", "api/main.py"]
