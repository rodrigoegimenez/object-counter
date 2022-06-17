FROM python:slim

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY counter/ app/

CMD [ "python", "-m", "counter.entrypoints.webapp" ]
