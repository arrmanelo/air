<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="bg-blue-600 text-white shadow-lg">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="text-3xl">🌍</div>
            <div>
              <h1 class="text-2xl font-bold">EcoMonitor Pavlodar</h1>
              <p class="text-sm text-blue-100">Умный экологический мониторинг в реальном времени</p>
            </div>
          </div>
          <div v-if="currentAQI" class="text-right">
            <div class="text-sm text-blue-100">Текущий AQI</div>
            <div class="text-3xl font-bold" :style="{ color: currentAQI.color }">
              {{ currentAQI.aqi }}
            </div>
            <div class="text-xs">{{ currentAQI.category }}</div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-6">
      <!-- Alert Banner -->
      <div v-if="activeAlerts.length > 0" class="mb-6">
        <div
          v-for="alert in activeAlerts.slice(0, 2)"
          :key="alert.id"
          :class="getAlertClass(alert.severity)"
          class="rounded-lg p-4 mb-2 flex items-center justify-between"
        >
          <div class="flex items-center">
            <span class="text-2xl mr-3">⚠️</span>
            <div>
              <div class="font-bold">{{ alert.severity.toUpperCase() }} ALERT</div>
              <div class="text-sm">{{ alert.message }}</div>
            </div>
          </div>
          <div class="text-xs">{{ formatTime(alert.timestamp) }}</div>
        </div>
      </div>

      <!-- Dashboard Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <!-- Main Stats -->
        <div class="lg:col-span-2 card">
          <h2 class="text-xl font-bold mb-4">📊 Текущие показатели</h2>
          <div v-if="loading" class="flex justify-center py-8">
            <div class="spinner"></div>
          </div>
          <div v-else-if="latestData" class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl mb-1">💨</div>
              <div class="text-sm text-gray-600">PM2.5</div>
              <div class="text-2xl font-bold">{{ latestData.pm25?.toFixed(1) || 'N/A' }}</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl mb-1">🌫️</div>
              <div class="text-sm text-gray-600">PM10</div>
              <div class="text-2xl font-bold">{{ latestData.pm10?.toFixed(1) || 'N/A' }}</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl mb-1">⚗️</div>
              <div class="text-sm text-gray-600">NO₂</div>
              <div class="text-2xl font-bold">{{ latestData.no2?.toFixed(1) || 'N/A' }}</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="text-center p-4 bg-gray-50 rounded-lg">
              <div class="text-2xl mb-1">🌡️</div>
              <div class="text-sm text-gray-600">Температура</div>
              <div class="text-2xl font-bold">{{ latestData.temperature?.toFixed(1) || 'N/A' }}</div>
              <div class="text-xs text-gray-500">°C</div>
            </div>
          </div>
        </div>

        <!-- AQI Info -->
        <div class="card">
          <h2 class="text-xl font-bold mb-4">🎯 Индекс качества воздуха</h2>
          <div v-if="currentAQI" class="text-center">
            <div
              class="aqi-badge text-4xl mb-3 inline-block"
              :style="{ backgroundColor: currentAQI.color }"
            >
              {{ currentAQI.aqi }}
            </div>
            <div class="text-lg font-bold mb-2">{{ currentAQI.category }}</div>
            <div class="text-sm text-gray-600">{{ currentAQI.health_message }}</div>
            <div class="mt-3 text-xs text-gray-500">
              Доминирующий загрязнитель: <strong>{{ currentAQI.dominant_pollutant }}</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Map and Sensors -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Map -->
        <div class="lg:col-span-2 card">
          <h2 class="text-xl font-bold mb-4">🗺️ Карта датчиков</h2>
          <div id="map" class="h-[500px] rounded-lg overflow-hidden bg-gray-200">
            <ClientOnly>
              <MapView :sensors="sensors" :latest-readings="latestReadings" />
            </ClientOnly>
          </div>
        </div>

        <!-- Active Sensors List -->
        <div class="card">
          <h2 class="text-xl font-bold mb-4">📡 Активные датчики</h2>
          <div v-if="sensors.length === 0" class="text-center text-gray-500 py-8">
            <div class="text-4xl mb-2">📡</div>
            <div>Нет активных датчиков</div>
          </div>
          <div v-else class="space-y-3 max-h-[450px] overflow-y-auto">
            <div
              v-for="sensor in sensors"
              :key="sensor.sensor_id"
              class="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition cursor-pointer"
            >
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-semibold">{{ sensor.name }}</div>
                  <div class="text-xs text-gray-600">{{ sensor.location_description }}</div>
                </div>
                <div
                  :class="sensor.status === 'active' ? 'bg-green-500' : 'bg-gray-400'"
                  class="w-3 h-3 rounded-full"
                ></div>
              </div>
              <div class="text-xs text-gray-500 mt-1">
                ID: {{ sensor.sensor_id }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Insights -->
      <div v-if="aiInsights" class="card mt-6">
        <h2 class="text-xl font-bold mb-4">🤖 AI Аналитика (Gemini)</h2>
        <div class="prose max-w-none">
          <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <div class="whitespace-pre-wrap">{{ aiInsights.insights }}</div>
          </div>
          <div class="mt-3 text-xs text-gray-500">
            Качество данных: {{ aiInsights.data_quality }} • Обновлено: {{ formatTime(aiInsights.timestamp) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white mt-12 py-8">
      <div class="container mx-auto px-4 text-center">
        <div class="text-sm">
          <p class="mb-2">🌍 Smart Environmental Monitoring System for Pavlodar</p>
          <p class="text-gray-400">Powered by Gemini AI • Pavlodar GDG Fest Hackathon 2025</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()

// State
const loading = ref(true)
const sensors = ref([])
const latestReadings = ref([])
const latestData = ref(null)
const currentAQI = ref(null)
const activeAlerts = ref([])
const aiInsights = ref(null)

// Fetch data
const fetchData = async () => {
  loading.value = true

  try {
    // Fetch sensors
    const sensorsRes = await fetch(`${config.public.iotApiUrl}/sensors`)
    const sensorsData = await sensorsRes.json()
    sensors.value = sensorsData.sensors || []

    // Fetch latest readings
    const readingsRes = await fetch(`${config.public.iotApiUrl}/readings/recent?limit=50`)
    const readingsData = await readingsRes.json()
    latestReadings.value = readingsData.readings || []

    if (latestReadings.value.length > 0) {
      latestData.value = latestReadings.value[0]
    }

    // Fetch current AQI
    const aqiRes = await fetch(`${config.public.analyticsApiUrl}/aqi/current`)
    const aqiData = await aqiRes.json()
    currentAQI.value = aqiData

    // Fetch active alerts
    const alertsRes = await fetch(`${config.public.alertApiUrl}/alerts/active`)
    const alertsData = await alertsRes.json()
    activeAlerts.value = alertsData.alerts || []

    // Fetch AI insights
    const insightsRes = await fetch(`${config.public.analyticsApiUrl}/insights`)
    const insightsData = await insightsRes.json()
    aiInsights.value = insightsData

  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

// Helpers
const getAlertClass = (severity) => {
  const classes = {
    critical: 'bg-red-100 border border-red-400 text-red-800',
    high: 'bg-orange-100 border border-orange-400 text-orange-800',
    medium: 'bg-yellow-100 border border-yellow-400 text-yellow-800',
    low: 'bg-blue-100 border border-blue-400 text-blue-800'
  }
  return classes[severity] || classes.low
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  fetchData()

  // Auto-refresh every 60 seconds
  setInterval(fetchData, 60000)
})
</script>
