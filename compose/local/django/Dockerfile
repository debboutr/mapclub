# pull official base image
FROM python:3.9.6-alpine


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc git python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#
# # install deepzoom.py
# RUN wget https://github.com/openzoom/deepzoom.py/archive/refs/heads/master.zip
# RUN unzip master.zip && mv deepzoom.py-master/ deepzoom/
# RUN pip install deepzoom/

# copy entrypoint.sh
COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# # copy project
# COPY . .
# set work directory
WORKDIR /app

# run entrypoint.sh
ENTRYPOINT ["/entrypoint"]
