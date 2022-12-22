# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /code/
RUN pip install -r requirements.txt
CMD ['python3' 'data_collection.py']
# COPY . /code/