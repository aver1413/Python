# Используйте официальный образ Python
FROM python:3.11

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y libyaml-dev libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей в образ
COPY requirements.txt /app/

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Определение переменной окружения для пути к базе данных SQLite
ENV DATABASE_PATH app/stat.db
ENV DATABASE_PATH app/db.sqlite3.db


# Копирование кода приложения в образ
COPY . /app/
EXPOSE 8080

# Смена рабочей директории на myproject web
#WORKDIR /app/myproject

# Смена рабочей директории на myproject bot
WORKDIR /app

# Запуск Django приложения

#CMD ["python3", "manage.py", "runserver_plus", "0.0.0.0:8000", "--cert-file", "localhost.crt"]

CMD ["python3", "manage.py", "runserver_plus", "0.0.0.0:8081", "--cert-file", "localhost.crt"]

#CMD ["python3", "bot.py"]
