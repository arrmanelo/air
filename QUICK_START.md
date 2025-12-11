# 🚀 Быстрый старт (Quick Start)

Простое руководство для запуска Weimea EcoMonitor с Google OAuth аутентификацией.

## 📋 Предварительные требования

- Docker и Docker Compose
- Google Cloud Console аккаунт (для OAuth)
- Gemini API ключ (для AI анализа)

## ⚡ Быстрая установка (5 минут)

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/weimea.git
cd weimea
```

### 2. Создайте Google OAuth credentials

1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект
3. Включите Google+ API
4. Создайте OAuth 2.0 Client ID:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8004/auth/google/callback`
5. Сохраните Client ID и Client Secret

### 3. Настройте переменные окружения

```bash
# Скопируйте пример файла
cp .env.example .env

# Отредактируйте .env и добавьте свои credentials
nano .env
```

Минимальная конфигурация:
```bash
GOOGLE_CLIENT_ID=ваш-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=ваш-client-secret
JWT_SECRET_KEY=случайная-строка-минимум-32-символа
GEMINI_API_KEY=ваш-gemini-api-ключ
```

### 4. Запустите приложение

```bash
# Запустите все сервисы
docker-compose up -d

# Проверьте статус
docker-compose ps
```

### 5. Откройте приложение

1. Frontend: http://localhost:3000
2. Auth API: http://localhost:8004
3. IoT API: http://localhost:8001
4. Analytics API: http://localhost:8002
5. Alert API: http://localhost:8003

## ✅ Проверка работы

### Тест аутентификации

1. Откройте http://localhost:3000
2. Нажмите "Login" или "Get Started"
3. Нажмите "Continue with Google"
4. Авторизуйтесь через Google
5. Вы будете перенаправлены в Dashboard

### Тест данных

Запустите симулятор сенсоров:
```bash
cd simulator
pip install -r requirements.txt
python sensor_simulator.py
```

Симулятор будет отправлять данные каждые 30 секунд. Обновите Dashboard, чтобы увидеть новые данные.

## 🔧 Полезные команды

```bash
# Просмотр логов всех сервисов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f auth_service

# Остановка всех сервисов
docker-compose down

# Полная очистка (включая данные)
docker-compose down -v

# Перезапуск сервиса
docker-compose restart auth_service

# Проверка базы данных
docker exec -it eco_postgres psql -U eco_monitor -d environmental_monitoring
```

## 📊 Структура сервисов

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Port 3000)                  │
│                  Nuxt.js + Vue 3 + Tailwind              │
└─────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Auth Service │    │  IoT Service │    │Analytics Svc │
│  (Port 8004) │    │  (Port 8001) │    │ (Port 8002)  │
│              │    │              │    │              │
│ Google OAuth │    │  Sensor Data │    │  AI Analysis │
│ JWT Tokens   │    │  MQTT        │    │  Gemini API  │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                ┌─────────────────────────┐
                │   PostgreSQL + TimescaleDB   │
                │        (Port 5432)       │
                └─────────────────────────┘
```

## 🎯 Что дальше?

1. **Настройка оповещений**: Настройте Firebase для push-уведомлений
2. **Добавление сенсоров**: Зарегистрируйте реальные IoT сенсоры
3. **Кастомизация**: Измените пороги для AQI и оповещений
4. **Мониторинг**: Добавьте Grafana для визуализации метрик

## 📚 Документация

- [Полная инструкция по настройке аутентификации](./SETUP_AUTH.md)
- [Основной README](./README.md)
- [Вклад в проект](./CONTRIBUTING.md)

## 🐛 Проблемы?

Самые частые проблемы и решения:

### "Invalid redirect URI"
✅ Добавьте `http://localhost:8004/auth/google/callback` в Google Cloud Console

### "Port already in use"
✅ Измените порты в `docker-compose.yml` или остановите конфликтующие сервисы

### "Database connection failed"
✅ Дождитесь полного запуска PostgreSQL (10-15 секунд) и перезапустите сервисы

### "Token verification failed"
✅ Проверьте, что `JWT_SECRET_KEY` задан в `.env` файле

## 💡 Подсказки

- Для разработки используйте `docker-compose logs -f` для отслеживания логов
- База данных хранится в Docker volume, данные сохраняются между перезапусками
- Для сброса базы: `docker-compose down -v && docker-compose up -d`
- Frontend работает в dev режиме с hot-reload

## 🤝 Поддержка

- GitHub Issues: https://github.com/yourusername/weimea/issues
- Email: support@weimea.com
- Documentation: https://docs.weimea.com

---

**Время установки:** ~5 минут
**Сложность:** Легко ⭐
**Требуется опыт:** Базовые знания Docker и командной строки
