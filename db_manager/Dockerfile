FROM python:3.8

WORKDIR /db_manager

COPY ./requirements.txt /db_manager/requirements.txt
COPY .env /db_manager/.env
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /db_manager/requirements.txt

#
COPY . /db_manager/

#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1235"]
CMD ["python", "main.py"]
