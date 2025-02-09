FROM python:3.10-slim

WORKDIR /app

# Скопируем файлы зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное в контейнер
COPY . .

# По умолчанию в docker-compose команда запуска будет 
# указана в разделе command