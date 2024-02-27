# pull the official docker image
FROM python:3.11-alpine

RUN apk add build-base git gcc musl-dev linux-headers python3-dev gettext

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /deps

COPY backend/Pipfile ./
RUN pipenv install --system --verbose --skip-lock

COPY docker/images/scripts/entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

RUN apk add yarn

ENTRYPOINT ["/bin/entrypoint.sh"]

WORKDIR /app
