FROM python:3.7-alpine
MAINTAINER Sameera Priya
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /student_app
WORKDIR /student_app
COPY ./student_app /student_app

RUN adduser -D user
USER user
