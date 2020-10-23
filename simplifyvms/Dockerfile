# Use the official Python image from the Docker Hub
FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y libmariadb-dev gcc

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Make a new directory to put our code in.
RUN mkdir /code/
RUN mkdir /code/logs

# Copy the requirements.txt file.
COPY ./requirements.txt /code/

# Change the working directory. 
# Every command after this will be run from the /code directory.
WORKDIR /code

# Copy the settings file
COPY simplifyvms/settings.yaml.example simplifyvms/settings.yaml

# Upgrade pip
RUN pip install --upgrade pip

# Install the requirements.
RUN pip install --use-feature=2020-resolver -r requirements.txt

# Copy the rest of the code. 
COPY . /code/ 

ENTRYPOINT ["/code/start.sh"]

# Adding ports
EXPOSE 8000