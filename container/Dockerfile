FROM python:3.8

RUN apt-get update && apt-get install build-essential

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY *.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --timeout 0 main:application