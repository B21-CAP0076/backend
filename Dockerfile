FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_URL 'mongodb://<user>:<password>@<IP>:27017/'
ENV DB_NAME 'habit'
ENV SERVER_PORT 8080
ENV SERVER_HOST '127.0.0.1'

COPY pip-requirements.txt .

RUN pip install -r pip-requirements.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port 8080