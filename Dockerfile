FROM python:3.11-alpine

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 443
CMD ./gunicorn.sh
