# pull official base image
FROM python:3.10-slim as development_build


# set work directory
WORKDIR /benny
COPY pyproject.toml poetry.lock ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
# RUN poetry install -n --no-ansi
RUN poetry check --lock && PIP_IGNORE_INSTALLED=1 PIP_USER=1 poetry install

EXPOSE 8000
# copy project
COPY . /benny/