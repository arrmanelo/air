# 🔐 Настройка аутентификации (Authentication Setup)

Этот документ описывает, как настроить Google OAuth аутентификацию для Weimea EcoMonitor.

## 📋 Содержание

- [Создание Google OAuth credentials](#создание-google-oauth-credentials)
- [Настройка переменных окружения](#настройка-переменных-окружения)
- [Запуск приложения](#запуск-приложения)
- [Тестирование](#тестирование)

## 🔑 Создание Google OAuth credentials

### Шаг 1: Создайте проект в Google Cloud Console

1. Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Название проекта: например, "Weimea EcoMonitor"

### Шаг 2: Включите Google+ API

1. В боковом меню выберите "APIs & Services" → "Library"
2. Найдите "Google+ API"
3. Нажмите "Enable"

### Шаг 3: Создайте OAuth 2.0 credentials

1. В боковом меню выберите "APIs & Services" → "Credentials"
2. Нажмите "Create Credentials" → "OAuth client ID"
3. Если требуется, настройте OAuth consent screen:
   - User Type: External
   - App name: Weimea EcoMonitor
   - User support email: ваш email
   - Developer contact: ваш email
   - Добавьте scopes: `openid`, `email`, `profile`
   - Add test users: добавьте ваш email для тестирования

4. Создайте OAuth client ID:
   - Application type: **Web application**
   - Name: "Weimea Auth Service"
   - Authorized redirect URIs:
     ```
     http://localhost:8004/auth/google/callback
     http://localhost:3000/auth/callback
     ```
   - Для продакшена добавьте:
     ```
     https://api.weimea.com/auth/google/callback
     https://weimea.com/auth/callback
     ```

5. Нажмите "Create"
6. Сохраните **Client ID** и **Client Secret**

## ⚙️ Настройка переменных окружения

### 1. Создайте файл `.env`

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

### 2. Заполните переменные окружения

Откройте `.env` и добавьте ваши credentials:

```bash
# Google OAuth (required for authentication)
GOOGLE_CLIENT_ID=ваш-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=ваш-client-secret

# JWT Secret Key (change in production)
JWT_SECRET_KEY=ваш-секретный-ключ-смените-в-продакшене

# PostgreSQL Configuration
POSTGRES_USER=eco_monitor
POSTGRES_PASSWORD=eco_pass
POSTGRES_DB=environmental_monitoring

# Gemini API Key (required)
GEMINI_API_KEY=your-gemini-api-key-here
```

**⚠️ ВАЖНО:**
- Никогда не коммитьте файл `.env` в git
- В продакшене используйте сложный `JWT_SECRET_KEY` (минимум 32 символа)
- Храните credentials в безопасном месте

## 🚀 Запуск приложения

### Запуск с Docker Compose (рекомендуется)

```bash
# Запустите все сервисы
docker-compose up -d

# Проверьте логи
docker-compose logs -f auth_service
```

### Запуск без Docker (для разработки)

#### 1. Запустите PostgreSQL

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=eco_monitor \
  -e POSTGRES_PASSWORD=eco_pass \
  -e POSTGRES_DB=environmental_monitoring \
  -p 5432:5432 \
  timescale/timescaledb:latest-pg15
```

#### 2. Запустите Auth Service

```bash
cd backend/auth_service
pip install -r requirements.txt
python main.py
```

Auth service будет доступен на `http://localhost:8004`

#### 3. Запустите Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на `http://localhost:3000`

## ✅ Тестирование

### 1. Проверьте работу Auth Service

Откройте в браузере:
```
http://localhost:8004
```

Вы должны увидеть JSON с информацией о сервисе.

### 2. Проверьте Google OAuth

1. Откройте `http://localhost:3000/login`
2. Нажмите "Continue with Google"
3. Вас перенаправит на страницу авторизации Google
4. После успешной авторизации вы будете перенаправлены в Dashboard

### 3. Проверьте токен

В консоли браузера (F12 → Console):

```javascript
// Проверьте токен в localStorage
console.log(localStorage.getItem('authToken'))

// Проверьте текущего пользователя
fetch('http://localhost:8004/auth/me', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('authToken')
  }
})
.then(r => r.json())
.then(console.log)
```

## 🔍 Структура базы данных

Auth service автоматически создаст таблицу `users` со следующей структурой:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    profile_picture VARCHAR,
    google_id VARCHAR UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP DEFAULT NOW(),
    is_active INTEGER DEFAULT 1,
    role VARCHAR DEFAULT 'user',
    extra_data JSON
);
```

## 🛠️ API Endpoints

Auth service предоставляет следующие endpoints:

- `GET /` - Информация о сервисе
- `GET /health` - Health check
- `GET /auth/google/login` - Начать Google OAuth flow
- `GET /auth/google/callback` - Обработать callback от Google
- `GET /auth/verify` - Проверить JWT токен (требует авторизации)
- `GET /auth/me` - Получить данные текущего пользователя (требует авторизации)
- `POST /auth/logout` - Выход (удаление токена на клиенте)

## 🔐 Безопасность

### JWT токены

- Токены действительны 7 дней
- Токены хранятся в `localStorage` браузера
- При каждом запросе к защищённым endpoints токен отправляется в header `Authorization: Bearer <token>`

### CORS

Auth service настроен на работу с:
- `http://localhost:3000` (frontend для разработки)
- `http://localhost:8080` (альтернативный порт)
- Настраиваемый `FRONTEND_URL` для продакшена

## 🐛 Решение проблем

### Проблема: "Invalid redirect URI"

Убедитесь, что в Google Cloud Console добавлены правильные Authorized redirect URIs:
- `http://localhost:8004/auth/google/callback`

### Проблема: "Unauthorized redirect"

Проверьте, что вы добавили себя как test user в OAuth consent screen.

### Проблема: "Token verification failed"

1. Проверьте, что `JWT_SECRET_KEY` одинаковый во всех сервисах
2. Убедитесь, что токен не истёк (7 дней)
3. Проверьте, что токен отправляется в правильном формате: `Bearer <token>`

### Проблема: База данных не подключается

1. Проверьте, что PostgreSQL запущен: `docker ps | grep postgres`
2. Проверьте переменные окружения `POSTGRES_*`
3. Проверьте логи: `docker-compose logs postgres`

## 📚 Дополнительная информация

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - для декодирования и проверки JWT токенов

## 🤝 Поддержка

Если у вас возникли проблемы, создайте issue в репозитории или свяжитесь с командой разработки.
