"""
Shared database utilities for PostgreSQL with TimescaleDB
"""
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database configuration
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'eco_monitor')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'eco_pass')}@"
    f"{os.getenv('POSTGRES_HOST', 'postgres')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB', 'environmental_monitoring')}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SensorReading(Base):
    """Sensor readings table (TimescaleDB hypertable)"""
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    pm25 = Column(Float)  # PM2.5 (µg/m³)
    pm10 = Column(Float)  # PM10 (µg/m³)
    no2 = Column(Float)   # NO₂ (µg/m³)
    co = Column(Float)    # CO (mg/m³)
    o3 = Column(Float)    # O₃ (µg/m³)
    so2 = Column(Float)   # SO₂ (µg/m³)
    temperature = Column(Float)  # °C
    humidity = Column(Float)     # %
    pressure = Column(Float)     # hPa
    extra_data = Column(JSON)  # Additional metadata (renamed from 'metadata' - reserved word)


class Sensor(Base):
    """Sensor registry table"""
    __tablename__ = "sensors"

    sensor_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_description = Column(String)
    sensor_type = Column(String)  # stationary, mobile
    status = Column(String, default="active")  # active, inactive, maintenance
    last_seen = Column(DateTime)
    extra_data = Column(JSON)  # Additional metadata (renamed from 'metadata' - reserved word)


class Alert(Base):
    """Environmental alerts table"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    alert_type = Column(String, nullable=False)  # pollution_spike, anomaly, threshold_exceeded
    severity = Column(String, nullable=False)    # low, medium, high, critical
    pollutant = Column(String)  # pm25, pm10, no2, etc.
    value = Column(Float)
    threshold = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    area = Column(String)  # district/area name
    message = Column(String)
    resolved = Column(Integer, default=0)  # 0 = active, 1 = resolved
    extra_data = Column(JSON)  # Additional metadata (renamed from 'metadata' - reserved word)


class User(Base):
    """Users table for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    profile_picture = Column(String)
    google_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    role = Column(String, default="user")  # user, admin, moderator
    extra_data = Column(JSON)  # Additional user metadata


def get_db():
    """Dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

    # Enable TimescaleDB extension and create hypertable
    with engine.connect() as conn:
        try:
            conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
            conn.execute(
                "SELECT create_hypertable('sensor_readings', 'timestamp', "
                "if_not_exists => TRUE);"
            )
            conn.commit()
            print("✅ Database initialized with TimescaleDB")
        except Exception as e:
            print(f"⚠️ TimescaleDB setup skipped (may already exist): {e}")
