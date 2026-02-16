# AI Car Consultant Bot

Интеллектуальный Telegram-бот для консультаций по подбору и привозу автомобилей с интеграцией GPT, RAG и квалификацией лидов.

## Возможности
- Естественный диалог и контекстная консультация.
- Расчет полной стоимости под ключ.
- Поиск по базе знаний через RAG (ChromaDB + embeddings).
- Квалификация лидов и передача менеджерам.
- Асинхронная архитектура для стабильной работы 24/7.

## Структура
Проект разделен на модули `ai/`, `bot/`, `services/`, `database/`, `knowledge_base/`, `utils/`, `tests/`.

## Быстрый старт
1. Скопируйте конфигурацию:
   ```bash
   cp .env.example .env
   ```
2. Заполните `.env` переменные.
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите инфраструктуру:
   ```bash
   docker compose up -d postgres redis
   ```
5. Запустите бота:
   ```bash
   python main.py
   ```

## Docker (полный запуск)
```bash
docker compose up --build
```

## Миграции Alembic
- Конфиг: `alembic.ini`
- Папка миграций: `database/migrations/versions`

## Тестирование
```bash
pytest -q
```

## Производственные рекомендации
- Включить мониторинг токенов и лимитов OpenAI.
- Хранить секреты в безопасном secret-store.
- Разнести worker-задачи (Celery) и Telegram polling/webhook по отдельным сервисам.
- Настроить алерты по Redis/PostgreSQL и ошибкам API.
