# 🌍 Smart Environmental Monitoring System

**Умная система экологического мониторинга для Павлодарской области**

Интеллектуальная система круглосуточного отслеживания качества воздуха в реальном времени с использованием IoT-датчиков, AI-аналитики (Gemini) и гиперлокального мониторинга загрязнений.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Nuxt 3](https://img.shields.io/badge/Nuxt-3.x-00DC82.svg)](https://nuxt.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4.svg)](https://deepmind.google/technologies/gemini/)

---

## 📖 О проекте

Система создана для решения проблемы экологического мониторинга в Павлодарской области — промышленном регионе Казахстана с высоким уровнем выбросов от НПЗ, ТЭС и заводов.

**Проблема:** В Павлодаре нет развернутой сети "умного" экологического мониторинга. Существующие посты далеки друг от друга и не дают гиперлокальной картины загрязнений.

**Решение:** Система IoT-датчиков + AI-аналитика для:
- Круглосуточного мониторинга PM2.5, PM10, NO₂, CO, O₃, SO₂
- Выявления "горячих точек" загрязнения в реальном времени
- Прогнозирования всплесков загрязнений (Gemini AI)
- Оповещения населения и городских служб
- Обоснованного экологического планирования

---

## ✨ Ключевые преимущества

✅ **Гиперлокальный мониторинг** - данные по каждому микрорайону
✅ **Реальное время** - обновление каждые 30 секунд
✅ **AI-прогнозирование** - Gemini AI предсказывает всплески загрязнений
✅ **Выявление аномалий** - автоматическое обнаружение источников выбросов
✅ **Система оповещений** - push-уведомления для граждан и служб
✅ **Открытые данные** - публичная карта и API
✅ **Масштабируемость** - от города до всей области

---

## 🎯 Функционал

### Для граждан
- 🗺️ Интерактивная карта качества воздуха
- 📊 AQI (Air Quality Index) в реальном времени
- 🚨 Push-уведомления о превышении порогов
- 📈 Исторические данные и графики
- 💡 Рекомендации от AI (когда лучше гулять, проветривать и т.д.)

### Для городских служб
- 🎯 Локализация источников загрязнений
- 📡 Мониторинг всех датчиков на одной панели
- 🤖 AI-анализ трендов и прогнозы
- ⚠️ Система алертов с уровнями критичности
- 📊 Аналитика и отчеты

### Технические возможности
- IoT сенсоры с LoRaWAN/NB-IoT
- TimescaleDB для временных рядов
- Gemini AI для анализа и прогнозов
- Knowledge Graph экологических данных
- Firebase для real-time updates
- REST API для интеграций

---

## 🏗️ Архитектура системы

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Nuxt 3)                         │
│            Интерактивная карта + Дашборд                     │
│                  http://localhost:3000                       │
└──────────────┬───────────────────────────────────────────────┘
               │
               ├─────────────────┬────────────────┬────────────┐
               │                 │                │            │
               ▼                 ▼                ▼            ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
    │ IoT Service  │  │  Analytics   │  │    Alert     │    │
    │   :8001      │  │   Service    │  │   Service    │    │
    │              │  │    :8002     │  │    :8003     │    │
    │  Sensor      │  │              │  │              │    │
    │  Data        │  │  Gemini AI   │  │  Threshold   │    │
    │  Ingestion   │  │  Prediction  │  │  Monitoring  │    │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
           │                 │                 │            │
           ▼                 ▼                 ▼            ▼
    ┌────────────────────────────────────────────────────────┐
    │     PostgreSQL 15 + TimescaleDB Extension              │
    │     (Time-series sensor data + alerts)                 │
    └──────────────────┬─────────────────────────────────────┘
                       │
                       ▼
    ┌────────────────────────────────────────────────────────┐
    │            Firebase Firestore                           │
    │    (Real-time updates + sensor metadata)                │
    └─────────────────────────────────────────────────────────┘
```

---

## 🔧 Технологический стек

### Backend
- **FastAPI** - высокопроизводительные REST API
- **PostgreSQL 15** + **TimescaleDB** - хранение временных рядов
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация данных

### AI & Analytics
- **Google Gemini 2.0 Flash** - AI-анализ и прогнозирование
- **Gemini Embeddings** - векторизация данных
- **NumPy** - численные расчеты

### Frontend
- **Nuxt 3** - Vue.js framework с SSR
- **TailwindCSS** - utility-first CSS
- **Leaflet** - интерактивные карты
- **Chart.js** - графики и визуализации

### Infrastructure
- **Docker** & **Docker Compose** - контейнеризация
- **Firebase** - real-time updates и auth
- **Nginx** - reverse proxy (production)

### IoT (для реального развертывания)
- **LoRaWAN** / **NB-IoT** - передача данных
- **MQTT** - протокол IoT
- Датчики: PM2.5/PM10/NO₂/CO/O₃/SO₂

---

## 🚀 Быстрый старт

### Требования

- Docker & Docker Compose
- Python 3.11+ (для симулятора)
- Node.js 18+ (для разработки фронтенда)
- Gemini API Key ([получить здесь](https://makersuite.google.com/app/apikey))
- (Опционально) Firebase проект для аутентификации

### Установка за 5 минут

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/yourusername/eco-monitoring-pavlodar.git
cd eco-monitoring-pavlodar
```

2. **Настройте переменные окружения**
```bash
cp .env.example .env
nano .env
```

Добавьте ваш Gemini API Key:
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

3. **Запустите все сервисы одной командой**
```bash
docker-compose up -d --build
```

Это запустит:
- 🗄️ PostgreSQL (порт 5432)
- 📡 IoT Service (порт 8001) - прием данных от датчиков
- 📊 Analytics Service (порт 8002) - анализ с Gemini AI
- 🚨 Alert Service (порт 8003) - система оповещений
- 💬 Chat Service (порт 8005) - AI ассистент EcoGuide
- 🔐 Auth Service (порт 8004) - Google OAuth
- 🌐 Frontend (порт 3000) - веб-интерфейс

4. **Проверьте статус сервисов**
```bash
docker-compose ps
# Все сервисы должны быть в статусе "Up"
```

5. **Запустите симулятор датчиков** (в новом терминале)
```bash
cd simulator
pip install -r requirements.txt
python sensor_simulator.py
```

Симулятор:
- ✅ Регистрирует 5 датчиков в Павлодаре
- ✅ Отправляет данные каждые 30 секунд
- ✅ Генерирует реалистичные температуры по сезонам (зимой -10°C..-18°C!)
- ✅ Имитирует промзоны, парки, транспортные узлы

6. **Откройте приложение**

- 🏠 Главная: **http://localhost:3000**
- 📊 Дашборд: **http://localhost:3000/dashboard**
- 🤖 AI Ассистент: кнопка внизу справа

### Первый запуск - ЧТО ДЕЛАТЬ?

1. Откройте http://localhost:3000/dashboard
2. Подождите 30-60 секунд пока симулятор отправит данные
3. Обновите страницу (F5)
4. Вы увидите:
   - 🗺️ Карту Павлодара с 5 датчиками
   - 📊 Графики PM2.5, PM10, NO₂
   - 🌡️ Текущую температуру (зимой около -10°C)
   - 🤖 AI ассистента EcoGuide в правом нижнем углу

---

## 📡 API Документация

### IoT Service (http://localhost:8001)

#### Регистрация датчика
```bash
POST /sensor/register
Content-Type: application/json

{
  "sensor_id": "SENSOR_001",
  "name": "Центральный парк",
  "latitude": 52.2850,
  "longitude": 76.9650,
  "location_description": "Парк культуры и отдыха",
  "sensor_type": "stationary"
}
```

#### Отправка данных с датчика
```bash
POST /sensor/data
Content-Type: application/json

{
  "sensor_id": "SENSOR_001",
  "latitude": 52.2850,
  "longitude": 76.9650,
  "pm25": 35.5,
  "pm10": 50.2,
  "no2": 45.8,
  "co": 1.2,
  "temperature": 18.5,
  "humidity": 55.0
}
```

#### Получить список датчиков
```bash
GET /sensors
```

#### Последние показания
```bash
GET /readings/recent?limit=100
```

---

### Analytics Service (http://localhost:8002)

#### Текущий AQI
```bash
GET /aqi/current?latitude=52.2873&longitude=76.9674&radius_km=5
```

Ответ:
```json
{
  "aqi": 85,
  "category": "Moderate",
  "color": "#ffff00",
  "health_message": "Air quality is acceptable...",
  "dominant_pollutant": "PM2.5",
  "data_points": {
    "pm25": 28.5,
    "pm10": 45.2,
    "no2": 38.1
  }
}
```

#### Почасовая статистика
```bash
GET /statistics/hourly?hours=24
```

#### AI-прогноз загрязнений (Gemini)
```bash
POST /predict
Content-Type: application/json

{
  "area": "Pavlodar",
  "start_time": "2025-12-11T00:00:00Z"
}
```

#### Выявление аномалий
```bash
GET /anomalies?hours=24&threshold=2.0
```

#### AI-инсайты (Gemini)
```bash
GET /insights?area=Pavlodar
```

---

### Alert Service (http://localhost:8003)

#### Создать алерт
```bash
POST /alert/create
Content-Type: application/json

{
  "alert_type": "threshold_exceeded",
  "severity": "high",
  "pollutant": "pm25",
  "value": 155.5,
  "threshold": 55.0,
  "latitude": 52.2873,
  "longitude": 76.9674,
  "area": "Pavlodar",
  "message": "PM2.5 levels are VERY UNHEALTHY"
}
```

#### Активные алерты
```bash
GET /alerts/active?severity=high
```

#### Проверка порогов (должна вызываться периодически)
```bash
POST /monitor/check
```

#### История алертов
```bash
GET /alerts/history?days=7
```

---

## 🎨 Скриншоты

### Главная страница с картой
![Dashboard](docs/screenshots/dashboard.png)

### Карта датчиков в реальном времени
![Map](docs/screenshots/map.png)

### Система оповещений
![Alerts](docs/screenshots/alerts.png)

---

## 📊 Примеры использования

### 1. Регистрация и отправка данных с датчика

```python
import requests

# Регистрация
response = requests.post(
    "http://localhost:8001/sensor/register",
    json={
        "sensor_id": "SENSOR_NEW",
        "name": "Новый датчик",
        "latitude": 52.2900,
        "longitude": 76.9700,
        "location_description": "Тестовая локация",
        "sensor_type": "stationary"
    }
)

# Отправка данных
response = requests.post(
    "http://localhost:8001/sensor/data",
    json={
        "sensor_id": "SENSOR_NEW",
        "latitude": 52.2900,
        "longitude": 76.9700,
        "pm25": 42.5,
        "pm10": 68.2,
        "no2": 55.1,
        "co": 1.8,
        "temperature": 20.5,
        "humidity": 48.0
    }
)
```

### 2. Получение AI-инсайтов

```bash
curl http://localhost:8002/insights?area=Pavlodar
```

### 3. Мониторинг алертов

```bash
curl http://localhost:8003/alerts/active
```

---

## 🔍 Мониторинг и обслуживание

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f iot_service
docker-compose logs -f analytics_service
```

### Перезапуск сервиса
```bash
docker-compose restart iot_service
```

### Подключение к БД
```bash
docker-compose exec postgres psql -U eco_monitor -d environmental_monitoring
```

### Проверка данных
```sql
-- Количество записей
SELECT COUNT(*) FROM sensor_readings;

-- Последние показания
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10;

-- Активные алерты
SELECT * FROM alerts WHERE resolved = 0;
```

---

## 🚀 Деплой в продакшн

### 1. Настройка сервера

```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установите Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Клонируйте и настройте

```bash
git clone https://github.com/yourusername/eco-monitoring-pavlodar.git
cd eco-monitoring-pavlodar

# Настройте .env для продакшн
cp .env.example .env
nano .env
```

### 3. Настройте Nginx (reverse proxy)

```nginx
server {
    listen 80;
    server_name ecomonitor.pavlodar.kz;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/iot {
        proxy_pass http://localhost:8001;
    }

    location /api/analytics {
        proxy_pass http://localhost:8002;
    }

    location /api/alert {
        proxy_pass http://localhost:8003;
    }
}
```

### 4. Установите SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ecomonitor.pavlodar.kz
```

### 5. Запустите с автостартом

```bash
docker-compose up -d

# Настройте автозапуск при перезагрузке
sudo systemctl enable docker
```

---

## 🧪 Тестирование

### Юнит-тесты (TODO)
```bash
# Backend
cd backend/iot_service
pytest

# Frontend
cd frontend
npm run test
```

### Нагрузочное тестирование (TODO)
```bash
# С помощью locust
locust -f tests/load_test.py
```

---

## 🗺️ Roadmap

### Phase 1 (MVP) ✅
- [x] IoT Service для приема данных
- [x] Analytics Service с Gemini AI
- [x] Alert Service для оповещений
- [x] Frontend с картой
- [x] Симулятор датчиков
- [x] Docker конфигурация

### Phase 2 (Q1 2025)
- [ ] Интеграция с реальными IoT датчиками (LoRaWAN)
- [ ] Мобильное приложение (React Native)
- [ ] Telegram Bot для уведомлений
- [ ] Email/SMS оповещения
- [ ] Экспорт данных (CSV, JSON, API)

### Phase 3 (Q2 2025)
- [ ] Knowledge Graph визуализация
- [ ] Предиктивная аналитика (ML модели)
- [ ] Интеграция с метео-API
- [ ] Рекомендации для городских служб
- [ ] Multi-tenancy (несколько городов)

### Phase 4 (Q3 2025)
- [ ] Мобильные лаборатории (как в Глазго)
- [ ] Интеграция с городским транспортом
- [ ] Автоматическое регулирование трафика
- [ ] Citizen Science - датчики от жителей
- [ ] Открытый API для исследователей

---

## 🤝 Команда

Проект создан для **Pavlodar GDG Fest Hackathon 2025**

**Backend Development:** [Ваше имя]
**AI/ML Integration:** [Ваше имя]
**Frontend Development:** [Ваше имя]
**DevOps & Infrastructure:** [Ваше имя]

---

## 📜 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

## 🙏 Благодарности

Создано с использованием:
- **Google Gemini AI** - AI-аналитика и прогнозирование
- **TimescaleDB** - time-series database
- **Leaflet** - interactive maps
- **FastAPI** - modern Python web framework
- **Nuxt 3** - Vue.js framework

Вдохновлено опытом:
- **Breathe London** - гиперлокальный мониторинг воздуха
- **Sensing the City (Glasgow)** - мобильные лаборатории
- **AirKaz** - общественный мониторинг в Казахстане

---

## 📞 Контакты

**Сайт:** https://ecomonitor.pavlodar.kz (coming soon)
**Email:** info@ecomonitor.kz
**Telegram:** @ecomonitor_pavlodar
**GitHub:** https://github.com/yourusername/eco-monitoring-pavlodar

---

<div align="center">

**🌍 Чистый воздух — право каждого. Данные — первый шаг к изменениям.**

Made with ❤️ in Pavlodar, Kazakhstan

</div>
