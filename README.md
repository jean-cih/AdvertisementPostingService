# Advertisement Posting Service

FastAPI-сервис для размещения объявлений с аутентификацией пользователей и администраторскими функциями.

## 🚀 Технологии

- Python 3.9+
- FastAPI (асинхронный веб-фреймворк)
- SQLite (база данных)
- SQLAlchemy 2.0 (ORM с асинхронной поддержкой)
- Pydantic (валидация данных)
- Uvicorn (ASGI-сервер)

## 📦 Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/yourusername/advertisement-posting-service.git
cd advertisement-posting-service
```
2. Создайте и активируйте виртуальное окружение:
```
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```
pip install -r requirements.txt
```

4. 🏃 Запуск
```
uvicorn src.main:app --reload
```
Сервер будет доступен по адресу: http://127.0.0.1:8000

📚 API Документация
После запуска доступны:
Swagger UI: /docs

🗄️ Структура проекта
requirements.txt

src/

├── main.py            # Точка входа

├── database.py        # Настройки базы данных

├── models/            # Модели SQLAlchemy

├── schemas/           # Pydantic схемы

├── api/

│     ├── endpoints/     # Роутеры API

│   │     ├── auth.py    # Аутентификация

│   │     ├── adverts.py # Объявления

│   │     └── admin.py   # Админ-панель

├── core/              # Основные настройки

│     ├── config.py      # Конфигурация

│     └── security.py    # JWT-аутентификация

└── services/          # Бизнес-логика

## 🔒 Аутентификация
Сервис использует JWT токены. Для доступа к защищенным эндпоинтам:
Зарегистрируйтесь через /auth/register
Авторизуйтесь через /auth/login

## 🛠️ Функционал
Пользователь:
- Регистрация и авторизация
- Создание/просмотр/удаление объявлений
- Просмотр всех объявлений с фильтрацией
Администратор:
- Все функции пользователя
- Управление пользователями (назначение админов, блокировка)
- Удаление любых комментариев
- Просмотр жалоб

## 📝 Лицензия
jean_cih
