# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]