FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN poetry install --no-interaction --no-ansi

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

CMD while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do sleep 0.1; done && \
    flask db upgrade && \
    flask run --host=0.0.0.0
