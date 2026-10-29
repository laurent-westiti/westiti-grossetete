# Image du service Westiti Grosse Tête.
FROM python:3.13-slim

WORKDIR /app
COPY service/requirements.txt /app/service/requirements.txt
RUN pip install --no-cache-dir -r /app/service/requirements.txt

COPY service /app/service
COPY site /app/site

# Le registre des commandes et les photos vivent dans /data, qui doit être un
# volume Railway : sans lui, ils disparaîtraient à chaque redéploiement.
#
# Pas d'instruction VOLUME ici, volontairement : Railway la refuse et gère ses
# volumes lui-même. Le volume se crée depuis le plan du projet (clic droit sur
# le fond, ou ⌘K puis « volume »), rattaché à ce service, chemin /data.
ENV WG_DONNEES=/data WG_PRODUCTION=1
EXPOSE 8000
WORKDIR /app/service

# Forme « shell », afin que $PORT imposé par Railway soit bien remplacé.
# Les en-têtes du proxy de Railway sont lus, pour que le site sache qu'il est
# servi en https : les adresses de retour de Stripe en dépendent.
CMD uvicorn app:application --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips="*"
