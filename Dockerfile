FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Connect to DB with credentials
ENV DB_URL 'mongodb://<user>:<password>@<IP>:27017/'
# If you are running in local without password, comment the line above use this instead by uncommenting: 
# ENV DB_URL 'mongodb://localhost:27017/' 

ENV DB_NAME 'habit'
ENV SERVER_PORT 8080
ENV SERVER_HOST '127.0.0.1'

COPY pip-requirements.txt .

RUN pip install -r pip-requirements.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port 8080
