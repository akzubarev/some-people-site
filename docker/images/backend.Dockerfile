# pull the official docker image
FROM python:3.11-alpine

RUN apk add --no-cache --upgrade ca-certificates ca-certificates-bundle

RUN apk add build-base git gcc musl-dev linux-headers python3-dev gettext

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --no-cache-dir --no-deps 'https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70'
RUN pip install pipenv

WORKDIR /deps

COPY backend/Pipfile ./
RUN pipenv install --system --verbose --skip-lock

COPY docker/images/scripts/entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT ["/bin/sh", "/bin/entrypoint.sh"]

WORKDIR /app
