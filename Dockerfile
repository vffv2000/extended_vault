FROM python:3.13-slim

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Рабочая директория
WORKDIR /project

# Копируем pyproject и lock-файл
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Копируем проект
COPY . .

# Указываем PYTHONPATH для всех процессов
ENV PYTHONPATH=/project/src

# CMD для main-app, Celery будет запускаться через docker-compose
CMD ["python", "src/main.py"]
