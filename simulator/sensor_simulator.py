"""
IoT Sensor Simulator
Simulates multiple environmental sensors sending data to the IoT Service
"""
import requests
import random
import time
from datetime import datetime
import json

# Configuration
IOT_API_URL = "http://localhost:8001"
NUM_SENSORS = 5

# Pavlodar area coordinates
PAVLODAR_CENTER = {"lat": 52.2873, "lon": 76.9674}
RADIUS = 0.05  # ~5km radius

# Sensor locations (industrial zones, residential areas, etc.)
SENSOR_LOCATIONS = [
    {
        "sensor_id": "SENSOR_001",
        "name": "Центральный парк",
        "lat": 52.2850,
        "lon": 76.9650,
        "description": "Центральный парк культуры и отдыха",
        "type": "stationary"
    },
    {
        "sensor_id": "SENSOR_002",
        "name": "Промзона НПЗ",
        "lat": 52.3200,
        "lon": 76.9500,
        "description": "Промышленная зона возле НПЗ",
        "type": "stationary"
    },
    {
        "sensor_id": "SENSOR_003",
        "name": "ЖК Достык",
        "lat": 52.2750,
        "lon": 76.9800,
        "description": "Жилой комплекс Достык",
        "type": "stationary"
    },
    {
        "sensor_id": "SENSOR_004",
        "name": "Автовокзал",
        "lat": 52.2900,
        "lon": 76.9700,
        "description": "Автовокзал (высокий трафик)",
        "type": "stationary"
    },
    {
        "sensor_id": "SENSOR_005",
        "name": "Мобильная станция",
        "lat": 52.2950,
        "lon": 76.9600,
        "description": "Мобильная лаборатория",
        "type": "mobile"
    }
]


def register_sensors():
    """Register all sensors in the system"""
    print("📡 Регистрация датчиков...")

    for sensor in SENSOR_LOCATIONS:
        try:
            response = requests.post(
                f"{IOT_API_URL}/sensor/register",
                json={
                    "sensor_id": sensor["sensor_id"],
                    "name": sensor["name"],
                    "latitude": sensor["lat"],
                    "longitude": sensor["lon"],
                    "location_description": sensor["description"],
                    "sensor_type": sensor["type"]
                }
            )

            if response.status_code == 200:
                print(f"   ✅ {sensor['name']} зарегистрирован")
            elif response.status_code == 400:
                print(f"   ℹ️  {sensor['name']} уже существует")
            else:
                print(f"   ❌ Ошибка регистрации {sensor['name']}: {response.text}")

        except Exception as e:
            print(f"   ❌ Ошибка подключения: {e}")

    print()


def generate_realistic_data(sensor_location, time_of_day):
    """
    Generate realistic environmental data based on location and time
    """
    # Base pollution levels (lower at night, higher during day)
    hour = datetime.now().hour
    month = datetime.now().month
    is_daytime = 7 <= hour <= 22
    is_rush_hour = hour in [8, 9, 17, 18, 19]

    # Location-specific factors
    is_industrial = "Промзона" in sensor_location["name"]
    is_traffic = "Автовокзал" in sensor_location["name"]
    is_park = "парк" in sensor_location["name"]

    # Base values
    base_pm25 = 15.0
    base_pm10 = 25.0
    base_no2 = 30.0
    base_co = 0.5

    # Adjust for time of day
    if is_daytime:
        base_pm25 *= 1.5
        base_pm10 *= 1.5
        base_no2 *= 1.8
        base_co *= 1.6

    if is_rush_hour:
        base_pm25 *= 1.3
        base_pm10 *= 1.2
        base_no2 *= 2.0
        base_co *= 1.8

    # Adjust for location
    if is_industrial:
        base_pm25 *= 2.5
        base_pm10 *= 2.0
        base_no2 *= 1.5
        base_co *= 1.3

    if is_traffic:
        base_pm25 *= 1.8
        base_no2 *= 2.5
        base_co *= 2.0

    if is_park:
        base_pm25 *= 0.5
        base_pm10 *= 0.6
        base_no2 *= 0.7
        base_co *= 0.7

    # Add random variations
    pm25 = max(0, base_pm25 + random.gauss(0, base_pm25 * 0.2))
    pm10 = max(0, base_pm10 + random.gauss(0, base_pm10 * 0.2))
    no2 = max(0, base_no2 + random.gauss(0, base_no2 * 0.2))
    co = max(0, base_co + random.gauss(0, base_co * 0.2))

    # Occasionally add pollution spikes (5% chance)
    if random.random() < 0.05:
        spike_factor = random.uniform(1.5, 3.0)
        pm25 *= spike_factor
        print(f"   ⚠️  Spike detected at {sensor_location['name']}!")

    # Temperature and humidity (realistic for Pavlodar by season)
    # Winter months (November - March): very cold
    # Spring (April - May): cool to warm
    # Summer (June - August): hot
    # Fall (September - October): cool

    if month in [11, 12, 1, 2, 3]:  # Winter - VERY COLD in Pavlodar
        if is_daytime:
            temperature = random.uniform(-8, -3)  # Day: -8°C to -3°C
            humidity = random.uniform(70, 85)  # Higher humidity in winter
        else:
            temperature = random.uniform(-18, -10)  # Night: -18°C to -10°C
            humidity = random.uniform(75, 90)
    elif month in [4, 5]:  # Spring
        if is_daytime:
            temperature = random.uniform(10, 20)
            humidity = random.uniform(40, 60)
        else:
            temperature = random.uniform(2, 10)
            humidity = random.uniform(50, 70)
    elif month in [6, 7, 8]:  # Summer
        if is_daytime:
            temperature = random.uniform(25, 35)  # Hot summers in Pavlodar
            humidity = random.uniform(25, 45)
        else:
            temperature = random.uniform(15, 22)
            humidity = random.uniform(35, 55)
    else:  # Fall (September, October)
        if is_daytime:
            temperature = random.uniform(8, 18)
            humidity = random.uniform(45, 65)
        else:
            temperature = random.uniform(-2, 8)
            humidity = random.uniform(55, 75)

    return {
        "sensor_id": sensor_location["sensor_id"],
        "latitude": sensor_location["lat"],
        "longitude": sensor_location["lon"],
        "pm25": round(pm25, 2),
        "pm10": round(pm10, 2),
        "no2": round(no2, 2),
        "co": round(co, 2),
        "o3": round(random.uniform(20, 80), 2),
        "so2": round(random.uniform(5, 30), 2),
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1),
        "pressure": round(random.uniform(1010, 1025), 1)
    }


def send_sensor_data():
    """Send data from all sensors"""
    print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] Отправка данных с датчиков...")

    for sensor in SENSOR_LOCATIONS:
        try:
            # Generate realistic data
            data = generate_realistic_data(sensor, datetime.now().hour)

            # Send to IoT Service
            response = requests.post(
                f"{IOT_API_URL}/sensor/data",
                json=data
            )

            if response.status_code == 200:
                status = "🟢"
                if data["pm25"] > 55:
                    status = "🔴"
                elif data["pm25"] > 35:
                    status = "🟡"

                print(f"   {status} {sensor['name']}: PM2.5={data['pm25']:.1f}, PM10={data['pm10']:.1f}, NO₂={data['no2']:.1f}")
            else:
                print(f"   ❌ Ошибка от {sensor['name']}: {response.text}")

        except Exception as e:
            print(f"   ❌ Ошибка подключения для {sensor['name']}: {e}")

    print()


def main():
    """Main simulation loop"""
    print("=" * 60)
    print("🌍 IoT Sensor Simulator - Pavlodar Environmental Monitoring")
    print("=" * 60)
    print()

    # Wait for services to be ready
    print("⏳ Ожидание запуска IoT Service...")
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{IOT_API_URL}/")
            if response.status_code == 200:
                print("✅ IoT Service готов!\n")
                break
        except:
            pass

        time.sleep(2)
        if i == max_retries - 1:
            print("❌ Не удалось подключиться к IoT Service")
            return

    # Register sensors
    register_sensors()

    # Continuous data sending
    print("🔄 Начинаем симуляцию (Ctrl+C для остановки)...\n")
    interval = 30  # seconds

    try:
        while True:
            send_sensor_data()
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n🛑 Симуляция остановлена")
        print("=" * 60)


if __name__ == "__main__":
    main()
