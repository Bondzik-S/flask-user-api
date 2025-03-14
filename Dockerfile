FROM python:3.12-slim

WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY pyproject.toml poetry.lock /app/

# Встановлюємо залежності через Poetry
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry install --no-interaction --no-ansi --no-root \
    && poetry add gunicorn  # Додаємо gunicorn

COPY . /app

# Створення користувача та зміна власника
RUN adduser -u 5678 --disabled-password --gecos "" appuser \
    && chown -R appuser /app

# Команда запуску
CMD ["python", "run.py"]
