# log8415-tp1

**Prerequisites:** [Python 3.11](https://www.python.org), [Poetry](https://python-poetry.org/) and [Docker](https://www.docker.com/)

## Web application

```sh
poetry install --only app
poetry run gunicorn app:app
```

Or with Docker:

```sh
docker build -t app -f app/Dockerfile .
docker run --rm -it -p 8000:8000 app
```

## Deployment

```sh
poetry install --only deploy
poetry run python3 -m deploy
```

## Benchmarking

```sh
poetry install --only bench
poetry run python3 -m bench
```

Or with Docker:

```sh
docker build -t bench -f bench/Dockerfile .
docker run --rm -it bench
```
