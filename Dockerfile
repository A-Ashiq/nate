# Pull a slim Python image
FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy the requirements into the current directory
COPY requirements.txt .

# Install dependencies
# Note that libpq-dev gcc is needed for psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt

COPY .. .