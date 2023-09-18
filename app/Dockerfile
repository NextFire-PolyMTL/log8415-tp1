FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip setuptools poetry~=1.6.0
COPY pyproject.toml poetry.lock ./
RUN poetry install --only app

COPY app/ .

ENTRYPOINT [ "poetry", "run", "gunicorn", "-b", "0.0.0.0", "app:app"]
EXPOSE 8000
