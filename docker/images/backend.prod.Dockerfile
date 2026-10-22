FROM python:3.11-alpine

RUN apk add --no-cache --upgrade ca-certificates ca-certificates-bundle

RUN apk add --no-cache \
    build-base \
    gettext \
    git \
    libffi-dev \
    linux-headers \
    musl-dev \
    python3-dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOG_DIR=/var/log/some-people

WORKDIR /deps
COPY backend/Pipfile backend/Pipfile.lock ./
RUN python -m pip install --no-cache-dir --no-deps 'https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70'
RUN pip install --no-cache-dir pipenv \
    && pipenv install --system --deploy \
    && pip uninstall --yes pipenv virtualenv virtualenv-clone \
    && rm -rf /root/.cache

WORKDIR /app
COPY backend/ ./

RUN addgroup -g 1001 app \
    && adduser -D -u 1001 -G app app \
    && mkdir -p /app/media /app/staticfiles /var/log/some-people \
    && chown -R app:app /app /var/log/some-people

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "config.wsgi:application"]
