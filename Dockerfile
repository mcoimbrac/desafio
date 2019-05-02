FROM python:3.7-alpine

ADD . /app

WORKDIR /app

RUN pip install troposphere

VOLUME [ "/app" ]

CMD [ "python", "/app/main.py" ]