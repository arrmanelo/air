# ⚠️ О ОШИБКАХ PYLANCE

Если вы видите ошибки в VS Code типа:
```
Import "sqlalchemy" could not be resolved
Import "fastapi" could not be resolved
```

## Это НОРМАЛЬНО! ✅

Эти ошибки появляются потому что:
- Python пакеты установлены **внутри Docker контейнеров**
- Ваша локальная IDE (VS Code/PyCharm) их не видит
- Это НЕ влияет на работу приложения!

## Как убрать эти ошибки? (опционально)

### Вариант 1: Игнорировать (рекомендуется)
Просто не обращайте внимания - приложение работает в Docker!

### Вариант 2: Установить зависимости локально
```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости всех сервисов
pip install -r backend/auth_service/requirements.txt
pip install -r backend/iot_service/requirements.txt
pip install -r backend/analytics_service/requirements.txt
pip install -r backend/alert_service/requirements.txt
```

### Вариант 3: Настроить Pylance
Создайте `.vscode/settings.json`:
```json
{
  "python.analysis.extraPaths": [
    "./backend/shared",
    "./backend/auth_service",
    "./backend/iot_service"
  ],
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "none"
  }
}
```

## Главное

**Приложение работает в Docker контейнерах!**
Все зависимости там установлены корректно.
Ошибки Pylance - это только локальная проблема IDE.

Просто запустите:
```bash
docker-compose up -d
```

И все будет работать! 🚀
