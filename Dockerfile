FROM python:3.8-slim

RUN apt-get update -y

RUN apt-get -y install wait-for-it

WORKDIR /mnt

COPY requirements/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod 755 data_collection/run.sh

ENTRYPOINT ["data_collection/run.sh"]
