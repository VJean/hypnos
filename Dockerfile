# Inspired from https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

FROM python:3.12 AS python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIRE=/tmp/poetry_cache \
    # read by installation script
    POETRY_VERSION=1.8.3 \
    # uwsgi
    # slim build: remove the need for libxml2 dependency
    # see https://github.com/unbit/uwsgi/issues/2687
    UWSGI_PROFILE_OVERRIDE="xml=false" \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
# https://github.com/orgs/python-poetry/discussions/1879#discussioncomment-216868

RUN pip install poetry==1.8.3

WORKDIR /app

COPY poetry.lock pyproject.toml ./
# Poetry will complain if a README.md is not found and as such we create an empty one.
# Copying the local one would effectively prevent Docker layer caching every time it is modified.
RUN touch README.md

# poetry install no-root to only install dependencies
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=python-base ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app ./app
COPY migrations ./migrations

ENTRYPOINT ["uwsgi", "--socket", "/shared/hypnos.sock", "--manage-script-name", "--module", "app:app", "--master", "--processes", "2"]
