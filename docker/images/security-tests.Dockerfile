FROM python:3.11-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --no-deps 'https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70'
WORKDIR /app
COPY backend/Pipfile /tmp/Pipfile
RUN python -c "import tomllib; p=tomllib.load(open('/tmp/Pipfile','rb'))['packages']; print('\n'.join(k+('['+','.join(v.get('extras',[]))+']' if v.get('extras') else '')+v['version'] if isinstance(v,dict) else k+v for k,v in p.items()))" > /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.txt
ENV DJANGO_SETTINGS_MODULE=config.security_test_settings PYTHONDONTWRITEBYTECODE=1
