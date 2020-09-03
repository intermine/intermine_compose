FROM python:3.8-alpine AS python-build-env
LABEL maintainer="Ank"

RUN apk update && apk add ca-certificates curl && apk add libpq postgresql-dev && apk add libffi-dev \
    && apk add build-base && rm -rf /var/cache/apk/*

WORKDIR /intermine_compose

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.5

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv venv

ADD pyproject.toml poetry.lock /intermine_compose/
RUN poetry export -f requirements.txt | venv/bin/pip install -r /dev/stdin

COPY . /intermine_compose
RUN poetry build && venv/bin/pip install dist/*.whl

FROM python:3.8-alpine
LABEL maintainer="Ank"
RUN apk update && apk add ca-certificates curl && apk add libpq postgresql-client
WORKDIR /intermine_compose
ENV PATH="/intermine_compose/venv/bin:$PATH"
COPY --from=python-build-env /intermine_compose/venv venv
RUN ls venv/bin/
EXPOSE 9991
CMD intermine_compose db init && intermine_compose run
