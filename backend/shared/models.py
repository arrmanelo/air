"""
Shared Pydantic models
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class SensorData(BaseModel):
    """Incoming sensor data model"""
    sensor_id: str
    timestamp: Optional[datetime] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    pm25: Optional[float] = Field(None, ge=0)
    pm10: Optional[float] = Field(None, ge=0)
    no2: Optional[float] = Field(None, ge=0)
    co: Optional[float] = Field(None, ge=0)
    o3: Optional[float] = Field(None, ge=0)
    so2: Optional[float] = Field(None, ge=0)
    temperature: Optional[float] = None
    humidity: Optional[float] = Field(None, ge=0, le=100)
    pressure: Optional[float] = None
    extra_data: Optional[Dict[str, Any]] = None


class SensorRegistration(BaseModel):
    """Sensor registration model"""
    sensor_id: str
    name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    location_description: str
    sensor_type: str = "stationary"  # stationary or mobile
    extra_data: Optional[Dict[str, Any]] = None


class AlertCreate(BaseModel):
    """Alert creation model"""
    alert_type: str
    severity: str
    pollutant: Optional[str] = None
    value: Optional[float] = None
    threshold: Optional[float] = None
    latitude: float
    longitude: float
    area: Optional[str] = None
    message: str
    extra_data: Optional[Dict[str, Any]] = None


class AQIResponse(BaseModel):
    """Air Quality Index response"""
    aqi: int
    category: str
    color: str
    health_message: str
    dominant_pollutant: str


class AnalysisRequest(BaseModel):
    """Analysis request model"""
    area: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    pollutants: Optional[List[str]] = None


class PredictionResponse(BaseModel):
    """Pollution prediction response"""
    prediction_time: datetime
    predicted_values: Dict[str, float]
    confidence: float
    factors: List[str]
    recommendations: List[str]
