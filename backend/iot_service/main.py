"""
IoT Service - Sensor Data Ingestion
Accepts data from IoT sensors via HTTP/MQTT
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.database import get_db, init_db, SensorReading, Sensor
from shared.models import SensorData, SensorRegistration
from shared.firebase_config import db as firestore_db

app = FastAPI(title="IoT Sensor Data Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("🚀 IoT Service started")


@app.get("/")
async def root():
    return {
        "service": "IoT Sensor Data Ingestion",
        "status": "operational",
        "version": "1.0.0"
    }


@app.post("/sensor/register")
async def register_sensor(
    sensor: SensorRegistration,
    db: Session = Depends(get_db)
):
    """
    Register a new sensor in the system
    """
    # Check if sensor already exists
    existing = db.query(Sensor).filter(Sensor.sensor_id == sensor.sensor_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Sensor already registered")

    new_sensor = Sensor(
        sensor_id=sensor.sensor_id,
        name=sensor.name,
        latitude=sensor.latitude,
        longitude=sensor.longitude,
        location_description=sensor.location_description,
        sensor_type=sensor.sensor_type,
        status="active",
        last_seen=datetime.utcnow(),
        metadata=sensor.metadata
    )

    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)

    # Also save to Firestore for quick access (if available)
    if firestore_db:
        try:
            firestore_db.collection('sensors').document(sensor.sensor_id).set({
                'sensor_id': sensor.sensor_id,
                'name': sensor.name,
                'latitude': sensor.latitude,
                'longitude': sensor.longitude,
                'location_description': sensor.location_description,
                'sensor_type': sensor.sensor_type,
                'status': 'active',
                'registered_at': datetime.utcnow(),
                'metadata': sensor.metadata or {}
            })
        except Exception as e:
            print(f"⚠️  Firestore update failed (non-critical): {e}")

    return {"message": "Sensor registered successfully", "sensor_id": sensor.sensor_id}


@app.post("/sensor/data")
async def ingest_sensor_data(
    data: SensorData,
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Ingest sensor data (from IoT devices)
    Accepts data via HTTP POST with optional API key authentication
    """
    # Validate sensor exists
    sensor = db.query(Sensor).filter(Sensor.sensor_id == data.sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found. Please register first.")

    # Create reading
    reading = SensorReading(
        sensor_id=data.sensor_id,
        timestamp=data.timestamp or datetime.utcnow(),
        latitude=data.latitude,
        longitude=data.longitude,
        pm25=data.pm25,
        pm10=data.pm10,
        no2=data.no2,
        co=data.co,
        o3=data.o3,
        so2=data.so2,
        temperature=data.temperature,
        humidity=data.humidity,
        pressure=data.pressure,
        metadata=data.metadata
    )

    db.add(reading)

    # Update sensor last seen
    sensor.last_seen = datetime.utcnow()

    db.commit()
    db.refresh(reading)

    # Store latest reading in Firestore for real-time access (if available)
    if firestore_db:
        try:
            firestore_db.collection('latest_readings').document(data.sensor_id).set({
                'sensor_id': data.sensor_id,
                'timestamp': reading.timestamp,
                'latitude': data.latitude,
                'longitude': data.longitude,
                'pm25': data.pm25,
                'pm10': data.pm10,
                'no2': data.no2,
                'co': data.co,
                'o3': data.o3,
                'so2': data.so2,
                'temperature': data.temperature,
                'humidity': data.humidity,
                'pressure': data.pressure,
                'metadata': data.metadata or {}
            })
        except Exception as e:
            print(f"⚠️  Firestore update failed (non-critical): {e}")

    return {
        "message": "Data ingested successfully",
        "reading_id": reading.id,
        "timestamp": reading.timestamp
    }


@app.get("/sensors")
async def list_sensors(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all registered sensors
    """
    query = db.query(Sensor)
    if status:
        query = query.filter(Sensor.status == status)

    sensors = query.all()
    return {
        "count": len(sensors),
        "sensors": [
            {
                "sensor_id": s.sensor_id,
                "name": s.name,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "location_description": s.location_description,
                "sensor_type": s.sensor_type,
                "status": s.status,
                "last_seen": s.last_seen
            }
            for s in sensors
        ]
    }


@app.get("/sensor/{sensor_id}/latest")
async def get_latest_reading(
    sensor_id: str,
    db: Session = Depends(get_db)
):
    """
    Get latest reading from a specific sensor
    """
    reading = db.query(SensorReading).filter(
        SensorReading.sensor_id == sensor_id
    ).order_by(SensorReading.timestamp.desc()).first()

    if not reading:
        raise HTTPException(status_code=404, detail="No readings found")

    return {
        "sensor_id": reading.sensor_id,
        "timestamp": reading.timestamp,
        "latitude": reading.latitude,
        "longitude": reading.longitude,
        "pm25": reading.pm25,
        "pm10": reading.pm10,
        "no2": reading.no2,
        "co": reading.co,
        "o3": reading.o3,
        "so2": reading.so2,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "pressure": reading.pressure
    }


@app.get("/readings/recent")
async def get_recent_readings(
    limit: int = 100,
    sensor_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get recent readings (for real-time monitoring)
    """
    query = db.query(SensorReading)

    if sensor_id:
        query = query.filter(SensorReading.sensor_id == sensor_id)

    readings = query.order_by(SensorReading.timestamp.desc()).limit(limit).all()

    return {
        "count": len(readings),
        "readings": [
            {
                "id": r.id,
                "sensor_id": r.sensor_id,
                "timestamp": r.timestamp,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "pm25": r.pm25,
                "pm10": r.pm10,
                "no2": r.no2,
                "co": r.co,
                "temperature": r.temperature,
                "humidity": r.humidity
            }
            for r in readings
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
