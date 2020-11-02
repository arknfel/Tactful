FROM python:3.6.6-alpine3.6

RUN apk update && apk add libressl-dev libffi-dev gcc musl-dev python3-dev



# FROM ubuntu:latest

# RUN apt-get update -y
# RUN apt-get -y upgrade
# RUN apt-get install -y python3-pip python3-dev
# RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
#     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","app.py"]