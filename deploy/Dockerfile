################################
# PYTHON-BASE
# Sets up all our shared environment variables
################################
FROM python:3.11.0-slim-bullseye as python-base
    # Python
ENV PYTHONUNBUFFERED=1 \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # Poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # never create virtual environment automaticly, only use env prepared by us
    POETRY_VIRTUALENVS_CREATE=false \
    \
    # this is where our requirements + virtual environment will live
    VIRTUAL_ENV="/venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

# prepare virtual env
RUN python -m venv $VIRTUAL_ENV

# working directory and Python path
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"

################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
################################
FROM python-base as builder-base

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  libsasl2-dev \
  libssl-dev \
  curl

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# The --mount will mount the buildx cache directory to where
# Poetry and Pip store their cache so that they can re-use it
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python -
RUN poetry config --list

WORKDIR /app

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /app/

# Allow installing dev dependencies to run tests
RUN  --mount=type=cache,target=/root/.cache  poetry install --no-root --only main

################################
# TESTING AND LINT
# Image used for test an lint
################################
FROM python-base as testing

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /app

RUN  --mount=type=cache,target=/root/.cache  poetry install --no-root

CMD ["bash"]


################################
# PRODUCTION
# Final image used for runtime
################################
FROM python-base as production

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR /app
# It could be easir to have the whole app in a /src directory
# Or add a dockerignore, but since this small it doesn't matter
COPY poetry.lock pyproject.toml manage.py  ./
COPY quizes/ ./quizes
COPY survey/ ./survey
COPY templates/ ./templates

COPY deploy/start ./
RUN chmod +x start

ENV GUNICORN_WORKERS=1
ENV GUNICORN_THREADS=1
ENV DEBUG=False
ENV DJANGO_SETTINGS_MODULE = "quizes.production"

RUN ls -a

EXPOSE 5000

CMD ["./start"]
