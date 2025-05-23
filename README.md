# LibraryAPI

LibraryAPI — это RESTful API, разработанный для управления библиотекой. Он предоставляет эндпоинты для работы с различными ресурсами, такими как книги, авторы и пользователи, что позволяет эффективно управлять данными библиотеки. API поддерживает аутентификацию, авторизацию и операции CRUD (Создание, Чтение, Обновление, Удаление), что упрощает интеграцию с фронтенд-приложениями или другими сервисами.

## Особенности
- Аутентификация пользователей и управление ролями (администратор и читатель)
- Управление книгами, авторами и записями о заимствовании
- Интеграция с базой данных для постоянного хранения
- Хорошо структурированные эндпоинты API для легкого доступа к ресурсам
- Тестирование для обеспечения надежности

## Установка

1. Клонируйте репозиторий, находясь в директории, куда хотите скачать проект:
   ```bash
   git clone https://github.com/s0wll/LibraryAPI.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd LibraryAPI
   ```
3. В корне проекта создайте файл .env и установите в нем следующие значения:
   ```bash
   MODE=LOCAL

   DB_HOST=library_db
   DB_PORT=5432
   DB_USER=library_user
   DB_PASS=library_password
   DB_NAME=LibraryAPI

   REDIS_HOST=library_redis_cache
   REDIS_PORT=6379

   JWT_SECRET_KEY=89d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
4. В папке src/tasks создайте файл config.py и установите в нем следующие значения:
   ```bash
   sender_email = "почта, с которой будет производиться отправка письма"
   sender_password = "пароль от этой почты"
   ```

## Запуск

Запустите Docker Compose с помощью следующей команды:
```bash
docker compose up --build
```

Для запуска приложения только с логами API, вместо команды выше выполните:
```bash
docker compose up -d --build
```
```bash
docker logs --follow library_back
```

## Документация

API документация доступна по адресу: http://localhost/docs

## Тестирование

1. Для проведения тестирования, в корне проекта необходимо создать дополнительный файл .env-test и установить в нем следующие значения:
   ```bash
   MODE=TEST

   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=(ваше имя пользователя postgres)
   DB_PASS=(ваш пароль postgres)
   DB_NAME=LibraryAPI-test

   REDIS_HOST=localhost
   REDIS_PORT=6379

   JWT_SECRET_KEY=89d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

2. Далее создайте дополнительную базу данных в PostgreSQL (локальное соединение) и назовите ее "LibraryAPI-test".

3. Далее создайте и запустите виртуальное окружение с помощью команд (Я использовал в разработке версию Python 3.13.1):
   ```bash
   python3 -m venv venv
   ```

   Для MacOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   Для Windows:
   ```bash
   venv\Scripts\activate.bat
   ```
   
   Не забудьте выбрать правильное venv в вашем редакторе кода (В случае с VSCode - это "Recommended").

4. Далее скачайте зависимости, выполнив команду:
   ```bash
   pip install -r requirements.txt
   ```

После этого, для запуска тестирования, выполните следующую команду:
```bash
pytest -v -s
```

Если возникнут проблемы с переменными окружения, то выполните следующие команды, чтобы сбросить их значения:
```bash
unset MODE
unset DB_HOST
unset DB_PORT
unset DB_USER
unset DB_PASS
unset DB_NAME
unset REDIS_HOST
```
