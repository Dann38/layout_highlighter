ARG REPOSITORY="docker.io"
FROM ubuntu:22.04

WORKDIR /tesseract

COPY ./requirements.txt /tesseract/requirements.txt

# install python3
RUN apt-get update && apt-get install -y python3 python3-pip software-properties-common ffmpeg libsm6 libxext6

# install tesseract
RUN add-apt-repository -y  ppa:alex-p/tesseract-ocr-devel && apt update --allow-releaseinfo-change && apt install -y tesseract-ocr tesseract-ocr-rus


RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade -r /tesseract/requirements.txt

#
COPY ./tesseract_reader /tesseract/tesseract_reader
#COPY ./setup.py /tesseract/setup.py
#RUN tesseract/setup.py install

COPY ./api /tesseract

CMD ["python3", "main.py"]
