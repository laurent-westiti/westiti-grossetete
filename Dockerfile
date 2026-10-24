# Image du service Westiti Grosse Tête.
FROM python:3.13-slim

WORKDIR /app
COPY service/requirements.txt /app/service/requirements.txt
RUN pip install --no-cache-dir -r /app/service/requirements.txt

COPY service /app/service
COPY site /app/site

ENV WG_PRODUCTION=1
EXPOSE 8000
WORKDIR /app/service

# Forme « shell », afin que $PORT imposé par Railway soit bien remplacé.
CMD uvicorn app:application --host 0.0.0.0 --port ${PORT:-8000}
