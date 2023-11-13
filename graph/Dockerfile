FROM python:3.8

COPY ./requirements.txt /graph/requirements.txt
COPY . /graph

COPY ./graph /graph/graph
COPY ./api /graph/api

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /graph/requirements.txt

WORKDIR /graph/api

ENTRYPOINT ["python"]
CMD ["main.py"]