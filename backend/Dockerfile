# Start the officially supported python3.9 library.
FROM python:3.10

WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the contents of requirements.txt to docker location.
COPY ./requirements.txt /code/requirements.txt

# Install the modules.
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy the contents of the application.
COPY ./app /code/app