FROM python:3.9.6-slim-bullseye
RUN apt-get -y update
RUN apt install -y build-essential \
                   libsndfile1 

RUN python -m pip install --upgrade pip

WORKDIR /
COPY app/requirements.txt requirements.txt
RUN pip install --default-timeout=100 -r requirements.txt

COPY app/ .

WORKDIR /

EXPOSE 5000

CMD uvicorn server:app --reload
