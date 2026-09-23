FROM python:3.11-alpine

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
RUN pip install --no-cache-dir --upgrade pip pipenv \
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
