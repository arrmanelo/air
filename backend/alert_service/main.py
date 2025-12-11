"""
Alert Service - Environmental Alert & Notification System
Monitors thresholds and sends alerts to citizens and authorities
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import Optional, List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.database import get_db, init_db, Alert, SensorReading
from shared.models import AlertCreate
from shared.firebase_config import db as firestore_db

app = FastAPI(title="Environmental Alert Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Alert thresholds (based on WHO and national standards)
THRESHOLDS = {
    "pm25": {
        "moderate": 35.0,
        "unhealthy": 55.0,
        "very_unhealthy": 150.0,
        "hazardous": 250.0
    },
    "pm10": {
        "moderate": 50.0,
        "unhealthy": 150.0,
        "very_unhealthy": 250.0,
        "hazardous": 350.0
    },
    "no2": {
        "moderate": 100.0,
        "unhealthy": 200.0,
        "very_unhealthy": 400.0,
        "hazardous": 800.0
    },
    "co": {
        "moderate": 9.0,
        "unhealthy": 15.0,
        "very_unhealthy": 30.0,
        "hazardous": 50.0
    }
}


def determine_severity(pollutant: str, value: float) -> str:
    """Determine alert severity based on pollutant value"""
    if pollutant not in THRESHOLDS:
        return "low"

    thresholds = THRESHOLDS[pollutant]

    if value >= thresholds["hazardous"]:
        return "critical"
    elif value >= thresholds["very_unhealthy"]:
        return "high"
    elif value >= thresholds["unhealthy"]:
        return "medium"
    elif value >= thresholds["moderate"]:
        return "low"
    else:
        return "info"


def generate_alert_message(pollutant: str, value: float, severity: str, area: str = None) -> str:
    """Generate human-readable alert message"""
    pollutant_names = {
        "pm25": "PM2.5",
        "pm10": "PM10",
        "no2": "Nitrogen Dioxide (NO₂)",
        "co": "Carbon Monoxide (CO)"
    }

    location = f" in {area}" if area else ""

    if severity == "critical":
        return f"⚠️ CRITICAL: {pollutant_names.get(pollutant, pollutant)} levels{location} are HAZARDOUS ({value:.1f} µg/m³). Stay indoors and close windows. Avoid all outdoor activities."
    elif severity == "high":
        return f"⚠️ HIGH: {pollutant_names.get(pollutant, pollutant)} levels{location} are VERY UNHEALTHY ({value:.1f} µg/m³). Sensitive groups should stay indoors. Everyone should reduce outdoor activities."
    elif severity == "medium":
        return f"⚠️ ALERT: {pollutant_names.get(pollutant, pollutant)} levels{location} are UNHEALTHY ({value:.1f} µg/m³). Sensitive groups should limit outdoor exposure."
    else:
        return f"ℹ️ Notice: {pollutant_names.get(pollutant, pollutant)} levels{location} are elevated ({value:.1f} µg/m³). Air quality is acceptable for most people."


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("🚀 Alert Service started")


@app.get("/")
async def root():
    return {
        "service": "Environmental Alert Service",
        "status": "operational",
        "version": "1.0.0"
    }


@app.post("/alert/create")
async def create_alert(
    alert: AlertCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new environmental alert
    """
    new_alert = Alert(
        timestamp=datetime.utcnow(),
        alert_type=alert.alert_type,
        severity=alert.severity,
        pollutant=alert.pollutant,
        value=alert.value,
        threshold=alert.threshold,
        latitude=alert.latitude,
        longitude=alert.longitude,
        area=alert.area,
        message=alert.message,
        resolved=0,
        metadata=alert.metadata
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    # Store in Firestore for real-time updates
    firestore_db.collection('alerts').document(str(new_alert.id)).set({
        'alert_id': new_alert.id,
        'timestamp': new_alert.timestamp,
        'alert_type': alert.alert_type,
        'severity': alert.severity,
        'pollutant': alert.pollutant,
        'value': alert.value,
        'latitude': alert.latitude,
        'longitude': alert.longitude,
        'area': alert.area,
        'message': alert.message,
        'resolved': False
    })

    # Send notifications in background
    background_tasks.add_task(send_notifications, new_alert)

    return {
        "message": "Alert created successfully",
        "alert_id": new_alert.id,
        "severity": alert.severity
    }


@app.get("/alerts/active")
async def get_active_alerts(
    severity: Optional[str] = None,
    area: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all active (unresolved) alerts
    """
    query = db.query(Alert).filter(Alert.resolved == 0)

    if severity:
        query = query.filter(Alert.severity == severity)

    if area:
        query = query.filter(Alert.area == area)

    alerts = query.order_by(Alert.timestamp.desc()).limit(50).all()

    return {
        "count": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "timestamp": a.timestamp,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "pollutant": a.pollutant,
                "value": a.value,
                "area": a.area,
                "message": a.message,
                "location": {"lat": a.latitude, "lon": a.longitude}
            }
            for a in alerts
        ]
    }


@app.post("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Mark an alert as resolved
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.resolved = 1
    db.commit()

    # Update Firestore
    firestore_db.collection('alerts').document(str(alert_id)).update({
        'resolved': True,
        'resolved_at': datetime.utcnow()
    })

    return {"message": "Alert resolved successfully"}


@app.post("/monitor/check")
async def check_thresholds(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Check recent readings against thresholds and create alerts if needed
    This should be called periodically (e.g., every 5 minutes)
    """
    # Check readings from last 15 minutes
    recent_time = datetime.utcnow() - timedelta(minutes=15)
    readings = db.query(SensorReading).filter(
        SensorReading.timestamp >= recent_time
    ).all()

    alerts_created = 0

    for reading in readings:
        # Check each pollutant
        for pollutant in ['pm25', 'pm10', 'no2', 'co']:
            value = getattr(reading, pollutant)

            if value is None:
                continue

            severity = determine_severity(pollutant, value)

            # Only create alerts for medium severity and above
            if severity in ['medium', 'high', 'critical']:
                # Check if similar alert already exists (avoid duplicates)
                threshold_key = 'moderate' if severity == 'medium' else 'unhealthy' if severity == 'high' else 'very_unhealthy'
                threshold_value = THRESHOLDS[pollutant].get(threshold_key, 0)

                existing = db.query(Alert).filter(
                    and_(
                        Alert.sensor_id == reading.sensor_id,
                        Alert.pollutant == pollutant,
                        Alert.timestamp >= datetime.utcnow() - timedelta(hours=1),
                        Alert.resolved == 0
                    )
                ).first()

                if not existing:
                    # Create alert
                    message = generate_alert_message(pollutant, value, severity)

                    alert = Alert(
                        timestamp=datetime.utcnow(),
                        alert_type="threshold_exceeded",
                        severity=severity,
                        pollutant=pollutant,
                        value=value,
                        threshold=threshold_value,
                        latitude=reading.latitude,
                        longitude=reading.longitude,
                        area="Pavlodar",  # Could be determined from coordinates
                        message=message,
                        resolved=0,
                        metadata={"sensor_id": reading.sensor_id}
                    )

                    db.add(alert)
                    alerts_created += 1

    db.commit()

    return {
        "message": "Threshold check completed",
        "readings_checked": len(readings),
        "alerts_created": alerts_created
    }


@app.get("/alerts/history")
async def get_alert_history(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get alert history for the past N days
    """
    start_time = datetime.utcnow() - timedelta(days=days)

    alerts = db.query(Alert).filter(
        Alert.timestamp >= start_time
    ).order_by(Alert.timestamp.desc()).all()

    # Group by severity
    by_severity = {}
    for alert in alerts:
        severity = alert.severity
        if severity not in by_severity:
            by_severity[severity] = 0
        by_severity[severity] += 1

    return {
        "period": f"Last {days} days",
        "total_alerts": len(alerts),
        "by_severity": by_severity,
        "recent_alerts": [
            {
                "id": a.id,
                "timestamp": a.timestamp,
                "severity": a.severity,
                "pollutant": a.pollutant,
                "value": a.value,
                "area": a.area,
                "resolved": bool(a.resolved)
            }
            for a in alerts[:20]
        ]
    }


async def send_notifications(alert: Alert):
    """
    Send notifications via various channels (background task)
    In production: integrate with FCM, email, SMS, Telegram, etc.
    """
    print(f"📢 Sending notification for alert {alert.id}")
    print(f"   Severity: {alert.severity}")
    print(f"   Message: {alert.message}")

    # Here you would integrate with:
    # - Firebase Cloud Messaging (FCM) for push notifications
    # - Email service (SendGrid, AWS SES)
    # - SMS gateway
    # - Telegram Bot API
    # - City emergency broadcast system

    # Example: Store in Firestore for web/mobile apps
    firestore_db.collection('notifications').add({
        'alert_id': alert.id,
        'timestamp': datetime.utcnow(),
        'severity': alert.severity,
        'message': alert.message,
        'area': alert.area,
        'sent': True
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
