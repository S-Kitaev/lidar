# Dockerfile
FROM python:3.10-slim

# собрать пакеты для psycopg2
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
      gcc libpq-dev python3-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# сначала только requirements — для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь проект в /app
COPY . .

# чтобы import app.* работал
ENV PYTHONPATH=/app

# если нужны статические файлы, они лежат в templates, монтируете /app/templates в StaticFiles
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]