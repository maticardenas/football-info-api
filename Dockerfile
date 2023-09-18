FROM python:3.11-alpine3.15

LABEL maintainer="cardenasmatias.1990@gmail.com"

ENV PYTHONUNBUFFERED 1


RUN apk update && apk add gcc && apk add g++ && apk add libffi-dev \
   && apk add bash && apk add vim && \
    apk add --update --no-cache postgresql-client build-base postgresql-dev musl-dev

WORKDIR /usr/football_api

COPY ./ ./

EXPOSE 8000

RUN pip install poetry
RUN poetry install -vvv --no-root

CMD ["poetry", "run", "python", "football_api/manage.py", "runserver", "0.0.0.0:8000"]