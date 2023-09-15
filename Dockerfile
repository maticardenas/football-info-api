FROM python:3.11-alpine3.15

LABEL maintainer="cardenasmatias.1990@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add gcc && apk add g++ && apk add libffi-dev \
   && apk add bash && apk add vim

COPY ./poetry.lock ./pyproject.toml ./
COPY ./football_api /football_api
WORKDIR /football_api
EXPOSE 8000

RUN pip install poetry
RUN poetry install -vvv --no-root
RUN adduser --disabled-password --no-create-home django-user

USER django-user