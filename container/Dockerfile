FROM python:3.9

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY *.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -r user

USER user

CMD exec gunicorn --bind :$PORT --workers 1 --timeout 0 main:application