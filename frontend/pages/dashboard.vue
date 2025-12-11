<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <!-- Header -->
    <header class="glass-dark shadow-sm sticky top-0 z-50">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <NuxtLink to="/" class="flex items-center space-x-3">
            <div class="text-3xl">🌍</div>
            <div>
              <h1 class="text-2xl font-bold text-gradient">EcoMonitor</h1>
              <p class="text-xs text-gray-600">Live Dashboard</p>
            </div>
          </NuxtLink>
          <div class="flex items-center space-x-4">
            <div class="text-sm text-gray-600">
              Last update: {{ lastUpdate }}
            </div>
            <button
              @click="refreshData"
              class="btn-hover px-4 py-2 glass border border-gray-200 rounded-full font-semibold"
            >
              🔄 Refresh
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center min-h-[60vh]">
        <div class="spinner"></div>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Current AQI Banner -->
        <div class="glass-dark rounded-3xl p-8 mb-8 card-hover fade-in">
          <div class="flex flex-col md:flex-row items-center justify-between">
            <div class="flex items-center space-x-6 mb-4 md:mb-0">
              <div
                class="w-32 h-32 rounded-full flex flex-col items-center justify-center text-white shadow-2xl pulse-slow"
                :style="{ background: currentAQI?.color }"
              >
                <div class="text-5xl font-bold">{{ currentAQI?.aqi || '--' }}</div>
                <div class="text-sm">AQI</div>
              </div>
              <div>
                <div class="text-sm text-gray-600">Air Quality Index</div>
                <div class="text-4xl font-bold mb-2">{{ currentAQI?.category || 'Loading...' }}</div>
                <div class="text-sm text-gray-600">{{ currentAQI?.dominant_pollutant || '' }}</div>
              </div>
            </div>
            <div class="glass rounded-2xl p-6 max-w-md">
              <div class="text-sm font-semibold mb-2">Health Recommendation</div>
              <div class="text-sm text-gray-600">{{ currentAQI?.health_message || 'Loading...' }}</div>
            </div>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          <div class="glass-dark rounded-2xl p-6 card-hover fade-in">
            <div class="flex items-center justify-between mb-3">
              <div class="text-3xl">💨</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="text-sm text-gray-600 mb-1">PM2.5</div>
            <div class="text-3xl font-bold">{{ latestData?.pm25?.toFixed(1) || 'N/A' }}</div>
          </div>

          <div class="glass-dark rounded-2xl p-6 card-hover fade-in animation-delay-100">
            <div class="flex items-center justify-between mb-3">
              <div class="text-3xl">🌫️</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="text-sm text-gray-600 mb-1">PM10</div>
            <div class="text-3xl font-bold">{{ latestData?.pm10?.toFixed(1) || 'N/A' }}</div>
          </div>

          <div class="glass-dark rounded-2xl p-6 card-hover fade-in animation-delay-200">
            <div class="flex items-center justify-between mb-3">
              <div class="text-3xl">⚗️</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="text-sm text-gray-600 mb-1">NO₂</div>
            <div class="text-3xl font-bold">{{ latestData?.no2?.toFixed(1) || 'N/A' }}</div>
          </div>

          <div class="glass-dark rounded-2xl p-6 card-hover fade-in animation-delay-300">
            <div class="flex items-center justify-between mb-3">
              <div class="text-3xl">🌡️</div>
              <div class="text-xs text-gray-500">°C</div>
            </div>
            <div class="text-sm text-gray-600 mb-1">Temperature</div>
            <div class="text-3xl font-bold">{{ latestData?.temperature?.toFixed(1) || 'N/A' }}</div>
          </div>
        </div>

        <!-- Map and Charts Row -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <!-- Interactive Map -->
          <div class="glass-dark rounded-3xl p-6 card-hover">
            <h3 class="text-xl font-bold mb-4">Sensor Network</h3>
            <div id="map" class="h-[400px] rounded-2xl overflow-hidden bg-gray-100"></div>
          </div>

          <!-- Hourly Trends Chart -->
          <div class="glass-dark rounded-3xl p-6 card-hover">
            <h3 class="text-xl font-bold mb-4">24-Hour Trends</h3>
            <canvas id="trendsChart" class="w-full h-[400px]"></canvas>
          </div>
        </div>

        <!-- AI Insights -->
        <div class="glass-dark rounded-3xl p-8 mb-8 card-hover" v-if="insights">
          <div class="flex items-center space-x-3 mb-4">
            <div class="text-3xl">🤖</div>
            <h3 class="text-2xl font-bold">AI-Powered Insights</h3>
          </div>
          <div class="glass rounded-2xl p-6">
            <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ insights }}</p>
          </div>
        </div>

        <!-- Active Alerts -->
        <div v-if="activeAlerts.length > 0" class="glass-dark rounded-3xl p-6 card-hover">
          <h3 class="text-xl font-bold mb-4 flex items-center space-x-2">
            <span>🚨</span>
            <span>Active Alerts</span>
          </h3>
          <div class="space-y-3">
            <div
              v-for="alert in activeAlerts"
              :key="alert.id"
              class="glass rounded-2xl p-4 flex items-start space-x-3"
            >
              <div class="text-2xl">⚠️</div>
              <div class="flex-1">
                <div class="font-semibold text-red-600">{{ alert.severity }} Alert</div>
                <div class="text-sm text-gray-700 mt-1">{{ alert.message }}</div>
                <div class="text-xs text-gray-500 mt-2">{{ formatTime(alert.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const config = useRuntimeConfig()

// State
const loading = ref(true)
const lastUpdate = ref('')
const currentAQI = ref(null)
const latestData = ref(null)
const sensors = ref([])
const activeAlerts = ref([])
const insights = ref('')
let map = null
let chart = null
let refreshInterval = null

// Format timestamp
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

// Fetch all dashboard data
const fetchDashboardData = async () => {
  try {
    // Fetch current AQI
    const aqiRes = await fetch(`${config.public.analyticsApiUrl}/aqi/current`)
    const aqiData = await aqiRes.json()
    currentAQI.value = aqiData

    // Fetch latest reading
    const readingsRes = await fetch(`${config.public.iotApiUrl}/readings/recent?limit=1`)
    const readingsData = await readingsRes.json()
    if (readingsData.readings && readingsData.readings.length > 0) {
      latestData.value = readingsData.readings[0]
    }

    // Fetch sensors
    const sensorsRes = await fetch(`${config.public.iotApiUrl}/sensors`)
    const sensorsData = await sensorsRes.json()
    sensors.value = sensorsData.sensors || []

    // Fetch active alerts
    const alertsRes = await fetch(`${config.public.alertApiUrl}/alerts/active`)
    const alertsData = await alertsRes.json()
    activeAlerts.value = alertsData.alerts || []

    // Fetch AI insights
    try {
      const insightsRes = await fetch(`${config.public.analyticsApiUrl}/insights`)
      const insightsData = await insightsRes.json()
      insights.value = insightsData.insights || ''
    } catch (e) {
      console.log('Insights not available yet')
    }

    lastUpdate.value = new Date().toLocaleTimeString()
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

// Initialize map
const initMap = async () => {
  if (typeof window === 'undefined') return

  try {
    const L = (await import('leaflet')).default
    await import('leaflet/dist/leaflet.css')

    // Create map centered on Pavlodar
    map = L.map('map').setView([52.2873, 76.9674], 12)

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    // Add sensor markers
    sensors.value.forEach(sensor => {
      const marker = L.marker([sensor.latitude, sensor.longitude]).addTo(map)
      marker.bindPopup(`
        <div class="p-2">
          <div class="font-bold">${sensor.name}</div>
          <div class="text-sm text-gray-600">${sensor.location_description}</div>
          <div class="text-xs text-gray-500 mt-1">ID: ${sensor.sensor_id}</div>
        </div>
      `)
    })
  } catch (error) {
    console.error('Error initializing map:', error)
  }
}

// Initialize chart
const initChart = async () => {
  if (typeof window === 'undefined') return

  try {
    const Chart = (await import('chart.js/auto')).default

    // Fetch hourly statistics
    const statsRes = await fetch(`${config.public.analyticsApiUrl}/statistics/hourly?hours=24`)
    const statsData = await statsRes.json()

    const ctx = document.getElementById('trendsChart')
    if (!ctx) return

    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: statsData.statistics?.map(s => new Date(s.hour).toLocaleTimeString()) || [],
        datasets: [
          {
            label: 'PM2.5',
            data: statsData.statistics?.map(s => s.avg_pm25) || [],
            borderColor: 'rgb(99, 102, 241)',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            tension: 0.4
          },
          {
            label: 'PM10',
            data: statsData.statistics?.map(s => s.avg_pm10) || [],
            borderColor: 'rgb(168, 85, 247)',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'µg/m³'
            }
          }
        }
      }
    })
  } catch (error) {
    console.error('Error initializing chart:', error)
  }
}

// Refresh data
const refreshData = async () => {
  loading.value = true
  await fetchDashboardData()
  if (chart) {
    chart.destroy()
    await initChart()
  }
  loading.value = false
}

// Mount lifecycle
onMounted(async () => {
  loading.value = true
  await fetchDashboardData()
  await initMap()
  await initChart()
  loading.value = false

  // Auto-refresh every 30 seconds
  refreshInterval = setInterval(fetchDashboardData, 30000)
})

// Cleanup
onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  if (map) {
    map.remove()
  }
  if (chart) {
    chart.destroy()
  }
})
</script>

<style scoped>
.animation-delay-100 {
  animation-delay: 0.1s;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-300 {
  animation-delay: 0.3s;
}
</style>
