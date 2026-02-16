# AI Car Consultant Bot

Интеллектуальный Telegram-бот для консультаций по подбору и привозу автомобилей с интеграцией GPT/OpenRouter, RAG и квалификацией лидов.

## Что уже готово
- Асинхронный Telegram-бот на `python-telegram-bot` 20.x.
- LLM-слой с переключением провайдера: **OpenAI** или **OpenRouter**.
- RAG на ChromaDB + embeddings.
- Калькулятор стоимости "под ключ" с детализацией.
- Docker и production compose для VPS-раскатки.

## Структура проекта
- `ai/` — LLM, prompts, RAG, инструменты.
- `bot/` — handlers, keyboards, middleware.
- `services/` — сервисная бизнес-логика.
- `database/` — SQLAlchemy-модели и репозитории.
- `knowledge_base/` — стартовая база знаний.
- `tests/` — unit-тесты.

## 1) Локальный запуск

### 1.1 Подготовка env
```bash
cp .env.example .env
```

Заполните минимум:
- `TELEGRAM_BOT_TOKEN`
- `LLM_PROVIDER` (`openai` или `openrouter`)
- `LLM_API_KEY`
- `DATABASE_URL`
- `REDIS_URL`

### 1.2 Запуск инфраструктуры
```bash
docker compose up -d postgres redis
```

### 1.3 Установка зависимостей и старт бота
```bash
pip install -r requirements.txt
python main.py
```

## 2) Быстрый запуск всего в Docker
```bash
docker compose up --build
```

## 3) Production запуск на VPS

### 3.1 Рекомендуемый порядок
1. Скопировать репозиторий на VPS.
2. Создать `.env` из `.env.example`.
3. Задать безопасные пароли `POSTGRES_PASSWORD`, ключи API и токены.
4. Запустить:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```
5. Проверить логи:
   ```bash
   docker compose -f docker-compose.prod.yml logs -f bot
   ```

### 3.2 Что важно для продакшна
- Делайте бэкапы PostgreSQL volume.
- Храните `.env` вне git.
- Добавьте внешний мониторинг (Uptime Kuma/Prometheus/Grafana).
- Переведите Telegram-бота на webhook, если нужна строгая perimeter-безопасность.

## 4) Переключение OpenAI/OpenRouter

### Вариант A: OpenAI
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=...
LLM_BASE_URL=
```

### Вариант B: OpenRouter
```env
LLM_PROVIDER=openrouter
LLM_MODEL=openai/gpt-4o-mini
LLM_API_KEY=...
LLM_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_SITE_URL=https://your-domain.example
OPENROUTER_APP_NAME=ai-car-consultant-bot
```

> Логика бота не меняется: меняется только провайдер и модель в env.

## 5) Тесты
```bash
pytest -q
```

## 6) Миграции
- Конфиг: `alembic.ini`
- Версии: `database/migrations/versions`

