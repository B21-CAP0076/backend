FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pip-requirements.txt .

RUN pip install -r pip-requirements.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port 8080
