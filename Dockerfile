FROM python:3.9.5-alpine3.13 as development_build

ARG APP_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  # build:
  BUILD_ONLY_PACKAGES='wget' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # dockerize:
  DOCKERIZE_VERSION=v0.6.1 \
  # poetry:
  POETRY_VERSION=1.1.5 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"


RUN apk update && apk add --update --no-cache --progress \
  git \
  bash \
  tini \
  openssl \
  gcc \
  musl-dev \
  curl \
  # Installing `dockerize` utility:
  # https://github.com/jwilder/dockerize
  && wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" && dockerize --version \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version \
  && rm -rf \
  /var/cache/apk/* \
  /root/.cache


WORKDIR /opt/app

# This is a special case. We need to run this script as an entry point:
COPY deploy/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x '/docker-entrypoint.sh'

# Copy only requirements, to cache them in docker layer
COPY ./poetry.lock ./pyproject.toml /opt/app/

# Project initialization:
RUN echo "$APP_ENV" \
  && poetry install \
    $(if [ "$APP_ENV" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi \
  # Upgrading pip, it is insecure, remove after `pip@21.1`
  && poetry run pip install -U pip \
  # Cleaning poetry installation's cache for production:
  && if [ "$APP_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi


ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]

FROM development_build AS production_build
COPY . /opt/app
