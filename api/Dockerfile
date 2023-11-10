FROM python:3.8-alpine

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt
COPY . /api

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]