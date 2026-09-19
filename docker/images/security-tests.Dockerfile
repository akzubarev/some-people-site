FROM python:3.11-slim
WORKDIR /app
COPY backend/Pipfile /tmp/Pipfile
RUN python -c "import tomllib; p=tomllib.load(open('/tmp/Pipfile','rb'))['packages']; print('\n'.join(k+('['+','.join(v.get('extras',[]))+']' if v.get('extras') else '')+v['version'] if isinstance(v,dict) else k+v for k,v in p.items()))" > /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.txt
ENV DJANGO_SETTINGS_MODULE=config.security_test_settings PYTHONDONTWRITEBYTECODE=1
