#!/bin/sh

WORKERS=10

if [ -f ./ssl/cert.crt ] && [ -f ./ssl/private.key ]; then
  eval $(egrep -v '^#' config.env | xargs) gunicorn -b :443 --limit-request-line 0 --certfile=./ssl/cert.crt --keyfile=./ssl/private.key -w ${WORKERS} src:webapp
else
  eval $(egrep -v '^#' config.env | xargs) gunicorn -b :80 --limit-request-line 0 -w ${WORKERS} src:webapp
fi
