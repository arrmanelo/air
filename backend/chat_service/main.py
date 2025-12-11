"""
AI Chat Assistant Service
Provides intelligent environmental recommendations using Gemini AI
"""
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import google.generativeai as genai

# Add parent directory to path for shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.database import get_db, SensorReading, Sensor, Alert

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="Weimea Chat Assistant", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class ChatMessage(BaseModel):
    message: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ChatResponse(BaseModel):
    response: str
    data: Optional[Dict[str, Any]] = None
    recommendations: List[str] = []


# Helper functions
def calculate_aqi(pm25: float = None, pm10: float = None, no2: float = None) -> Dict[str, Any]:
    """Calculate Air Quality Index"""
    aqi_values = []

    if pm25 is not None:
        if pm25 <= 12: aqi = 50
        elif pm25 <= 35.4: aqi = 100
        elif pm25 <= 55.4: aqi = 150
        elif pm25 <= 150.4: aqi = 200
        elif pm25 <= 250.4: aqi = 300
        else: aqi = 400
        aqi_values.append(("PM2.5", aqi))

    if pm10 is not None:
        if pm10 <= 54: aqi = 50
        elif pm10 <= 154: aqi = 100
        elif pm10 <= 254: aqi = 150
        elif pm10 <= 354: aqi = 200
        elif pm10 <= 424: aqi = 300
        else: aqi = 400
        aqi_values.append(("PM10", aqi))

    if not aqi_values:
        return {"aqi": 0, "category": "Unknown", "color": "#gray"}

    dominant = max(aqi_values, key=lambda x: x[1])
    aqi = dominant[1]

    if aqi <= 50:
        category = "Хороший"
        color = "#00e400"
    elif aqi <= 100:
        category = "Умеренный"
        color = "#ffff00"
    elif aqi <= 150:
        category = "Нездоровый для чувствительных групп"
        color = "#ff7e00"
    elif aqi <= 200:
        category = "Нездоровый"
        color = "#ff0000"
    elif aqi <= 300:
        category = "Очень нездоровый"
        color = "#8f3f97"
    else:
        category = "Опасный"
        color = "#7e0023"

    return {
        "aqi": aqi,
        "category": category,
        "color": color,
        "dominant_pollutant": dominant[0]
    }


def get_location_data(db: Session, location: str = None, lat: float = None, lon: float = None) -> Dict[str, Any]:
    """Get sensor data for specific location"""
    query = db.query(
        SensorReading.pm25,
        SensorReading.pm10,
        SensorReading.no2,
        SensorReading.co,
        SensorReading.o3,
        SensorReading.temperature,
        SensorReading.humidity,
        SensorReading.latitude,
        SensorReading.longitude,
        SensorReading.timestamp
    ).order_by(SensorReading.timestamp.desc())

    # Filter by location if provided
    if lat and lon:
        # Find nearest sensor (within ~1km radius)
        query = query.filter(
            and_(
                SensorReading.latitude.between(lat - 0.01, lat + 0.01),
                SensorReading.longitude.between(lon - 0.01, lon + 0.01)
            )
        )

    # Get latest reading
    latest = query.first()

    if not latest:
        return None

    # Calculate AQI
    aqi_info = calculate_aqi(latest.pm25, latest.pm10, latest.no2)

    return {
        "pm25": latest.pm25,
        "pm10": latest.pm10,
        "no2": latest.no2,
        "co": latest.co,
        "o3": latest.o3,
        "temperature": latest.temperature,
        "humidity": latest.humidity,
        "aqi": aqi_info["aqi"],
        "category": aqi_info["category"],
        "timestamp": latest.timestamp.isoformat() if latest.timestamp else None
    }


def get_active_alerts(db: Session, lat: float = None, lon: float = None) -> List[Dict]:
    """Get active environmental alerts for area"""
    query = db.query(Alert).filter(Alert.resolved == 0)

    if lat and lon:
        query = query.filter(
            and_(
                Alert.latitude.between(lat - 0.02, lat + 0.02),
                Alert.longitude.between(lon - 0.02, lon + 0.02)
            )
        )

    alerts = query.order_by(Alert.timestamp.desc()).limit(5).all()

    return [
        {
            "type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "pollutant": alert.pollutant,
            "value": alert.value
        }
        for alert in alerts
    ]


def generate_recommendations(aqi: int, data: Dict, alerts: List[Dict]) -> List[str]:
    """Generate health recommendations based on air quality"""
    recommendations = []

    if aqi <= 50:
        recommendations.append("✅ Качество воздуха отличное! Можно гулять без ограничений.")
        recommendations.append("🏃 Идеальное время для занятий спортом на улице.")
    elif aqi <= 100:
        recommendations.append("⚠️ Качество воздуха умеренное. Можно гулять, но ограничьте интенсивные нагрузки.")
        recommendations.append("👥 Чувствительным людям стоит сократить время на улице.")
    elif aqi <= 150:
        recommendations.append("🚨 Воздух нездоровый для чувствительных групп.")
        recommendations.append("⏱️ Рекомендую гулять не более 30-40 минут.")
        recommendations.append("😷 Детям, пожилым и людям с заболеваниями лучше остаться дома.")
    elif aqi <= 200:
        recommendations.append("❌ Качество воздуха нездоровое для всех!")
        recommendations.append("🏠 Рекомендую остаться дома или гулять максимум 15-20 минут.")
        recommendations.append("😷 Используйте маску при выходе на улицу.")
    else:
        recommendations.append("🚫 ОПАСНО! Воздух очень загрязнен!")
        recommendations.append("🏠 Настоятельно рекомендую остаться дома.")
        recommendations.append("🪟 Закройте окна и используйте воздухоочистители.")

    # Temperature-based recommendations
    if data.get("temperature"):
        temp = data["temperature"]
        if temp < 0:
            recommendations.append(f"❄️ Температура {temp}°C - оденьтесь тепло!")
        elif temp > 30:
            recommendations.append(f"🌡️ Температура {temp}°C - не забудьте воду и головной убор!")

    # Alert-based recommendations
    if alerts:
        severe_alerts = [a for a in alerts if a["severity"] in ["high", "critical"]]
        if severe_alerts:
            recommendations.append(f"⚠️ Активных оповещений: {len(severe_alerts)}. Будьте осторожны!")

    return recommendations


def create_ai_response(user_message: str, data: Dict, recommendations: List[str]) -> str:
    """Generate AI response using Gemini"""
    if not GEMINI_API_KEY:
        return "⚠️ AI ассистент временно недоступен. Вот данные и рекомендации по вашему запросу."

    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""Ты виртуальный эко-ассистент "EcoGuide" для системы мониторинга окружающей среды в Павлодаре, Казахстан.

Пользователь спрашивает: "{user_message}"

Данные о качестве воздуха:
- AQI (Индекс качества воздуха): {data.get('aqi', 'неизвестно')}
- Категория: {data.get('category', 'неизвестно')}
- PM2.5: {data.get('pm25', 'н/д')} µg/m³
- PM10: {data.get('pm10', 'н/д')} µg/m³
- NO₂: {data.get('no2', 'н/д')} µg/m³
- Температура: {data.get('temperature', 'н/д')}°C
- Влажность: {data.get('humidity', 'н/д')}%

Автоматические рекомендации:
{chr(10).join(f"- {rec}" for rec in recommendations)}

Твоя задача:
1. Дай короткий, дружелюбный ответ на русском языке (2-4 предложения)
2. Объясни текущую ситуацию с воздухом простым языком
3. Дай персонализированный совет с учетом вопроса пользователя
4. Используй эмодзи для наглядности
5. Будь позитивным, но честным

Не повторяй все данные - выбери главное. Говори тепло и по-человечески."""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Gemini API error: {e}")
        return f"На основе данных: AQI = {data.get('aqi')}, категория '{data.get('category')}'. " + " ".join(recommendations[:2])


# Routes
@app.get("/")
async def root():
    return {
        "service": "Weimea Chat Assistant",
        "status": "running",
        "features": [
            "AI-powered environmental recommendations",
            "Real-time air quality analysis",
            "Location-based advice",
            "Personalized health suggestions"
        ]
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "gemini_configured": bool(GEMINI_API_KEY)}


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Chat with AI assistant about environmental conditions
    """
    try:
        # Get location data
        location_data = get_location_data(
            db,
            location=message.location,
            lat=message.latitude,
            lon=message.longitude
        )

        if not location_data:
            return ChatResponse(
                response="😔 К сожалению, для указанной локации нет данных. Попробуйте другое место или подождите пока сенсоры соберут информацию.",
                data=None,
                recommendations=[]
            )

        # Get alerts
        alerts = get_active_alerts(db, message.latitude, message.longitude)

        # Generate recommendations
        recommendations = generate_recommendations(
            location_data["aqi"],
            location_data,
            alerts
        )

        # Generate AI response
        ai_response = create_ai_response(
            message.message,
            location_data,
            recommendations
        )

        return ChatResponse(
            response=ai_response,
            data=location_data,
            recommendations=recommendations
        )

    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/suggestions")
async def get_suggestions():
    """Get sample questions for users"""
    return {
        "suggestions": [
            "Какой сейчас воздух на улице Лермонтова?",
            "Можно ли гулять сегодня с ребенком?",
            "Безопасно ли бегать утром?",
            "Какое качество воздуха в центре города?",
            "Стоит ли открывать окна?",
            "Когда лучше выйти на прогулку?"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
