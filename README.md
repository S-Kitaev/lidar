# Lidar
HES LiDAR project 

## Запуск проекта

1. На данный момент это веб-приложение на **FastAPI** с **JWT-авторизацией** и базой данных **PostgreSQL** обернутое в Docker, далее это будет полноценный проект интернета вещей.

2. Чтобы запустить его:
   - Склонируйте репозиторий.
   - Перейдите в папку проекта.
   - Убедитесь, что у вас установлены **Docker** и **Docker Compose**.

3. Выполните команду:
   ```bash
   docker compose up --build
   
4. Сам API-сервер на порту 8000 внутри контейнера, проброшенном на порт 8001 хоста. Перейдите в браузере по ссылке:
   ```bash
   http://localhost:8001/

5. Для локального использования без Docker:
   - Создайте виртуальное окружение.
   - Установите зависимости из requirements.txt. 
   - Настройте .env с параметром DATABASE_URL. 
   - Запустите PostgreSQL (например, через Docker). 
   - Запустите сервер командой: 
   ```bash 
   uvicorn main:app --reload
