# set base image
FROM python:3.6.6-alpine3.6

# exposing container port 5000
EXPOSE 5000

# ensure that that python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# create and set the working directoy in the container
RUN mkdir /code
WORKDIR /code

# copy the dependancies file to the working directory
COPY requirements.txt /code/

# install dependancies
RUN pip install -r requirements.txt

COPY . /code/

# initiate and run the first migration, create database file
RUN flask db init && flask db migrate && flask db upgrade

RUN python createadmin.py

RUN rm createadmin.py

# run the flask application 
CMD ["flask","run","--host=0.0.0.0"]