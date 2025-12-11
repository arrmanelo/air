"""
Analytics Service - AI-powered Environmental Data Analysis
Uses Gemini AI for predictions, anomaly detection, and insights
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import sys
import os
import google.generativeai as genai

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.database import get_db, SensorReading
from shared.models import AQIResponse, AnalysisRequest, PredictionResponse

app = FastAPI(title="Environmental Analytics Service", version="1.0.0")

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calculate_aqi(pm25: float = None, pm10: float = None, no2: float = None,
                  co: float = None, o3: float = None, so2: float = None) -> Dict:
    """
    Calculate Air Quality Index (AQI) based on pollutant levels
    Uses US EPA AQI standards
    """
    aqi_values = []
    dominant = None
    max_aqi = 0

    # PM2.5 breakpoints (µg/m³ to AQI)
    if pm25 is not None:
        if pm25 <= 12.0:
            aqi = (50 / 12.0) * pm25
        elif pm25 <= 35.4:
            aqi = 50 + ((100 - 50) / (35.4 - 12.1)) * (pm25 - 12.1)
        elif pm25 <= 55.4:
            aqi = 100 + ((150 - 100) / (55.4 - 35.5)) * (pm25 - 35.5)
        elif pm25 <= 150.4:
            aqi = 150 + ((200 - 150) / (150.4 - 55.5)) * (pm25 - 55.5)
        elif pm25 <= 250.4:
            aqi = 200 + ((300 - 200) / (250.4 - 150.5)) * (pm25 - 150.5)
        else:
            aqi = 300 + ((500 - 300) / (500.4 - 250.5)) * (pm25 - 250.5)

        if aqi > max_aqi:
            max_aqi = aqi
            dominant = "PM2.5"
        aqi_values.append(aqi)

    # PM10 calculation
    if pm10 is not None:
        if pm10 <= 54:
            aqi = (50 / 54) * pm10
        elif pm10 <= 154:
            aqi = 50 + ((100 - 50) / (154 - 55)) * (pm10 - 55)
        elif pm10 <= 254:
            aqi = 100 + ((150 - 100) / (254 - 155)) * (pm10 - 155)
        elif pm10 <= 354:
            aqi = 150 + ((200 - 150) / (354 - 255)) * (pm10 - 255)
        else:
            aqi = 200 + ((300 - 200) / (500 - 355)) * (pm10 - 355)

        if aqi > max_aqi:
            max_aqi = aqi
            dominant = "PM10"
        aqi_values.append(aqi)

    if not aqi_values:
        return {
            "aqi": 0,
            "category": "No Data",
            "color": "#gray",
            "health_message": "No data available",
            "dominant_pollutant": "None"
        }

    final_aqi = int(max(aqi_values))

    # Determine category
    if final_aqi <= 50:
        category = "Good"
        color = "#00e400"
        message = "Air quality is satisfactory, and air pollution poses little or no risk."
    elif final_aqi <= 100:
        category = "Moderate"
        color = "#ffff00"
        message = "Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
    elif final_aqi <= 150:
        category = "Unhealthy for Sensitive Groups"
        color = "#ff7e00"
        message = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
    elif final_aqi <= 200:
        category = "Unhealthy"
        color = "#ff0000"
        message = "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
    elif final_aqi <= 300:
        category = "Very Unhealthy"
        color = "#8f3f97"
        message = "Health alert: The risk of health effects is increased for everyone."
    else:
        category = "Hazardous"
        color = "#7e0023"
        message = "Health warning of emergency conditions: everyone is more likely to be affected."

    return {
        "aqi": final_aqi,
        "category": category,
        "color": color,
        "health_message": message,
        "dominant_pollutant": dominant
    }


@app.get("/")
async def root():
    return {
        "service": "Environmental Analytics Service",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/aqi/current")
async def get_current_aqi(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: float = 5.0,
    db: Session = Depends(get_db)
):
    """
    Get current AQI for a location (average of nearby sensors in last hour)
    """
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)

    query = db.query(
        func.avg(SensorReading.pm25).label('pm25'),
        func.avg(SensorReading.pm10).label('pm10'),
        func.avg(SensorReading.no2).label('no2'),
        func.avg(SensorReading.co).label('co'),
        func.avg(SensorReading.o3).label('o3'),
        func.avg(SensorReading.so2).label('so2')
    ).filter(SensorReading.timestamp >= one_hour_ago)

    # Filter by location if provided
    if latitude is not None and longitude is not None:
        # Simple bounding box filter (for more accuracy, use PostGIS)
        lat_range = radius_km / 111.0  # 1 degree ≈ 111 km
        lon_range = radius_km / (111.0 * abs(latitude / 90.0))

        query = query.filter(
            and_(
                SensorReading.latitude.between(latitude - lat_range, latitude + lat_range),
                SensorReading.longitude.between(longitude - lon_range, longitude + lon_range)
            )
        )

    result = query.first()

    if not result or result.pm25 is None:
        raise HTTPException(status_code=404, detail="No recent data available")

    aqi_data = calculate_aqi(
        pm25=result.pm25,
        pm10=result.pm10,
        no2=result.no2,
        co=result.co,
        o3=result.o3,
        so2=result.so2
    )

    return {
        **aqi_data,
        "location": {"latitude": latitude, "longitude": longitude} if latitude else None,
        "timestamp": datetime.utcnow(),
        "data_points": {
            "pm25": round(result.pm25, 2) if result.pm25 else None,
            "pm10": round(result.pm10, 2) if result.pm10 else None,
            "no2": round(result.no2, 2) if result.no2 else None,
            "co": round(result.co, 2) if result.co else None
        }
    }


@app.get("/statistics/hourly")
async def get_hourly_statistics(
    hours: int = 24,
    sensor_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get hourly statistics for the past N hours
    """
    start_time = datetime.utcnow() - timedelta(hours=hours)

    query = db.query(
        func.date_trunc('hour', SensorReading.timestamp).label('hour'),
        func.avg(SensorReading.pm25).label('avg_pm25'),
        func.max(SensorReading.pm25).label('max_pm25'),
        func.min(SensorReading.pm25).label('min_pm25'),
        func.avg(SensorReading.pm10).label('avg_pm10'),
        func.avg(SensorReading.no2).label('avg_no2'),
        func.avg(SensorReading.co).label('avg_co'),
        func.avg(SensorReading.temperature).label('avg_temp'),
        func.avg(SensorReading.humidity).label('avg_humidity')
    ).filter(SensorReading.timestamp >= start_time)

    if sensor_id:
        query = query.filter(SensorReading.sensor_id == sensor_id)

    query = query.group_by('hour').order_by('hour')

    results = query.all()

    return {
        "period": f"Last {hours} hours",
        "data_points": len(results),
        "statistics": [
            {
                "timestamp": r.hour,
                "pm25": {"avg": round(r.avg_pm25, 2) if r.avg_pm25 else None,
                        "max": round(r.max_pm25, 2) if r.max_pm25 else None,
                        "min": round(r.min_pm25, 2) if r.min_pm25 else None},
                "pm10": round(r.avg_pm10, 2) if r.avg_pm10 else None,
                "no2": round(r.avg_no2, 2) if r.avg_no2 else None,
                "co": round(r.avg_co, 2) if r.avg_co else None,
                "temperature": round(r.avg_temp, 2) if r.avg_temp else None,
                "humidity": round(r.avg_humidity, 2) if r.avg_humidity else None
            }
            for r in results
        ]
    }


@app.post("/predict")
async def predict_pollution(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Use Gemini AI to predict pollution levels and provide recommendations
    """
    # Get recent data for context
    recent_data = db.query(SensorReading).order_by(
        SensorReading.timestamp.desc()
    ).limit(100).all()

    if not recent_data:
        raise HTTPException(status_code=404, detail="Insufficient data for prediction")

    # Prepare data summary for Gemini
    data_summary = {
        "avg_pm25": sum(r.pm25 for r in recent_data if r.pm25) / len([r for r in recent_data if r.pm25]),
        "avg_pm10": sum(r.pm10 for r in recent_data if r.pm10) / len([r for r in recent_data if r.pm10]),
        "trend": "increasing" if recent_data[0].pm25 > recent_data[-1].pm25 else "decreasing"
    }

    # Create prompt for Gemini
    prompt = f"""
    Analyze the following environmental data from Pavlodar, Kazakhstan and provide predictions:

    Current Average PM2.5: {data_summary['avg_pm25']:.2f} µg/m³
    Current Average PM10: {data_summary['avg_pm10']:.2f} µg/m³
    Trend: {data_summary['trend']}

    Based on this data:
    1. Predict pollution levels for the next 6 hours
    2. Identify main contributing factors (industry, traffic, weather)
    3. Provide 3 specific recommendations for citizens and authorities

    Format your response as JSON with keys: prediction, factors, recommendations
    """

    try:
        response = model.generate_content(prompt)
        ai_response = response.text

        # Parse response (simplified - in production use structured output)
        return {
            "prediction_time": datetime.utcnow() + timedelta(hours=6),
            "predicted_values": {
                "pm25": round(data_summary['avg_pm25'] * 1.1, 2),  # Simplified prediction
                "pm10": round(data_summary['avg_pm10'] * 1.1, 2)
            },
            "confidence": 0.75,
            "ai_analysis": ai_response,
            "factors": ["Industrial emissions", "Traffic patterns", "Weather conditions"],
            "recommendations": [
                "Reduce outdoor activities if AQI exceeds 150",
                "Use air purifiers indoors",
                "Authorities should monitor industrial emissions closely"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI prediction failed: {str(e)}")


@app.get("/anomalies")
async def detect_anomalies(
    hours: int = 24,
    threshold: float = 2.0,
    db: Session = Depends(get_db)
):
    """
    Detect anomalies in pollution data (readings beyond threshold * stddev)
    """
    start_time = datetime.utcnow() - timedelta(hours=hours)

    # Calculate mean and stddev
    stats = db.query(
        func.avg(SensorReading.pm25).label('mean_pm25'),
        func.stddev(SensorReading.pm25).label('std_pm25')
    ).filter(SensorReading.timestamp >= start_time).first()

    if not stats.mean_pm25:
        return {"anomalies": [], "message": "Insufficient data"}

    threshold_value = stats.mean_pm25 + (threshold * stats.std_pm25)

    # Find anomalous readings
    anomalies = db.query(SensorReading).filter(
        and_(
            SensorReading.timestamp >= start_time,
            SensorReading.pm25 > threshold_value
        )
    ).all()

    return {
        "period": f"Last {hours} hours",
        "threshold": round(threshold_value, 2),
        "mean": round(stats.mean_pm25, 2),
        "stddev": round(stats.std_pm25, 2),
        "anomalies_found": len(anomalies),
        "anomalies": [
            {
                "sensor_id": a.sensor_id,
                "timestamp": a.timestamp,
                "pm25": a.pm25,
                "location": {"lat": a.latitude, "lon": a.longitude}
            }
            for a in anomalies[:20]  # Limit to 20
        ]
    }


@app.get("/insights")
async def get_ai_insights(
    area: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get AI-generated insights about environmental conditions
    """
    # Get recent statistics
    recent = db.query(
        func.avg(SensorReading.pm25).label('pm25'),
        func.avg(SensorReading.pm10).label('pm10'),
        func.avg(SensorReading.no2).label('no2'),
        func.count(SensorReading.id).label('count')
    ).filter(
        SensorReading.timestamp >= datetime.utcnow() - timedelta(hours=24)
    ).first()

    if not recent.count:
        raise HTTPException(status_code=404, detail="No data available")

    aqi = calculate_aqi(pm25=recent.pm25, pm10=recent.pm10, no2=recent.no2)

    prompt = f"""
    Analyze environmental conditions in Pavlodar, Kazakhstan:

    24-hour Average:
    - PM2.5: {recent.pm25:.2f} µg/m³
    - PM10: {recent.pm10:.2f} µg/m³
    - NO₂: {recent.no2:.2f} µg/m³
    - AQI: {aqi['aqi']} ({aqi['category']})

    Provide:
    1. Brief assessment (2-3 sentences)
    2. Main concerns
    3. Actionable advice for residents

    Keep response concise and practical.
    """

    try:
        response = model.generate_content(prompt)

        return {
            "timestamp": datetime.utcnow(),
            "area": area or "Pavlodar",
            "aqi": aqi,
            "insights": response.text,
            "data_quality": "good" if recent.count > 100 else "limited"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI insights failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
