# intermine-compose

![Tests](https://github.com/intermine/intermine_compose/workflows/Tests/badge.svg)
![Coverage](https://github.com/intermine/intermine_compose/workflows/Coverage/badge.svg)


Repo to handle docker orchestration in the cloud

 ## **Note**

 Do **not** use master branch of this repo. Massive refactor going on.

Use **v1** branch instead.

## Getting started

#### Prerequisites

We assume a Mac or Linux environment; this has not been tested on Windows. 

Download and install: 

1. [PostgreSQL](https://www.postgresql.org/download/)
2. [Redis](https://redis.io/download)

> Note : These instructions assume that:
>- you have a local instance of **postgres** and **redis** running
>- your postgres user has access to a table named composedb (in your terminal, once you have postgres installed run `createdb composedb`)
>
> and that you will be using the *development* configuration:
>- your postgres user is `postgres` with password `postgres`
>
> You can change the defaults in `config/development.py` or the variable FLASK_CONFIG_MODE to select another configuration (see `config` directory).
>
> In particular to configure all parameters please use the *production* configuration and define the parameters (PGUSER, PGPASSWORD and PGHOST) in the .env file

### Create an environment file
Create a .env file in the root of repo and add these:
```bash
# change values as needed
FLASK_CONFIG_MODE=development
CONFIGURATOR_URL=http://localhost:9999/
KUBE_ENABLE=False
IM_DATA_DIR=/tmp/sharedfs

SQLALCHEMY_DATABASE_URI="postgres://postgres:postgres@localhost:5432/curation"
# URI is formatted as "postgres://USERNAME:PASSWORD@HOST:PORT/DATABASE"
# Make sure to create this database on your postgres server manually.
```

### Create a virtual environment(optional but recommended)
Create a python virtual environment
```bash
conda create -n intermine_compose python=3.8 && conda activate intermine_compose
```

### Install poetry

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Install dependencies
```bash
poetry install
```

### Install Pre commit hooks(Only if you want to develop)

This installs hooks for running python's black formatter and flake8 lint

```bash
pre-commit install
```

### Setup database

Use `intermine_compose` cli to init database

```bash
intermine_compose db init
```

### Start server

```bash
intermine_compose run
```

### Nox

Run tests, lint check, type check, doc tests, coverage
```bash
nox -rs
```

### Build docs
```bash
nox -rs docs
```

You can find compiled docs in `docs/_build` dir.

OpenAPI spec is located at `docs/openapi.yml`.

### Docker (optional)

Use docker and docker-compose to run server.

```bash
docker-compose up --force-recreate --build
```

> Note: If the build fails with an error message `Warning: The lock file is not up to date with the latest changes in pyproject.toml. You may be getting outdated dependencies. Run update to update them`, then do `poetry update` and rebuild container.

The default path for this app is http://localhost:9991/ 
