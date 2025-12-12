<template>
  <div class="min-h-screen">
    <!-- Hero Section with Animated Background -->
    <div class="relative overflow-hidden">
      <!-- Animated Gradient Blobs -->
      <div class="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div class="absolute top-20 left-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-20 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <!-- Header -->
      <header class="relative z-10 glass-dark shadow-sm">
        <div class="container mx-auto px-4 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="text-3xl">🌍</div>
              <div>
                <h1 class="text-2xl font-bold text-gradient">EcoMonitor</h1>
                <p class="text-xs text-gray-600">Pavlodar Smart City</p>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <NuxtLink to="/login" class="text-gray-700 hover:text-gray-900 transition">
                Sign In
              </NuxtLink>
              <NuxtLink
                to="/dashboard"
                class="btn-hover px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full font-semibold glow"
              >
                Get Started →
              </NuxtLink>
            </div>
          </div>
        </div>
      </header>

      <!-- Hero Content -->
      <div class="relative z-10 container mx-auto px-4 py-20">
        <div class="max-w-4xl mx-auto text-center fade-in">
          <h1 class="text-6xl md:text-7xl font-bold mb-6 leading-tight">
            Your air quality,
            <span class="text-gradient block mt-2">intelligently monitored.</span>
          </h1>
          <p class="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
            Experience real-time environmental monitoring powered by AI.
            Track pollution levels, get instant alerts, and breathe easier.
          </p>
          <div class="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
            <NuxtLink
              to="/dashboard"
              class="btn-hover px-8 py-4 bg-black text-white rounded-full font-semibold text-lg inline-flex items-center space-x-2"
            >
              <span>Start Free Trial</span>
              <span>→</span>
            </NuxtLink>
            <button
              @click="scrollToDashboard"
              class="btn-hover px-8 py-4 glass border border-gray-200 rounded-full font-semibold text-lg"
            >
              View Live Demo
            </button>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-6 mt-20 max-w-3xl mx-auto">
          <div class="glass-dark rounded-2xl p-6 text-center card-hover">
            <div class="text-4xl font-bold text-gradient mb-2">24/7</div>
            <div class="text-sm text-gray-600">Real-time Monitoring</div>
          </div>
          <div class="glass-dark rounded-2xl p-6 text-center card-hover">
            <div class="text-4xl font-bold text-gradient mb-2">{{ sensors.length }}+</div>
            <div class="text-sm text-gray-600">Active Sensors</div>
          </div>
          <div class="glass-dark rounded-2xl p-6 text-center card-hover">
            <div class="text-4xl font-bold text-gradient mb-2">AI</div>
            <div class="text-sm text-gray-600">Powered Analytics</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16 fade-in">
          <h2 class="text-5xl font-bold mb-4">Why EcoMonitor?</h2>
          <p class="text-xl text-gray-600">Everything you need for environmental monitoring</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="glass-dark rounded-3xl p-8 card-hover">
            <div class="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center text-3xl mb-6">
              🎯
            </div>
            <h3 class="text-2xl font-bold mb-3">Hyperlocal Data</h3>
            <p class="text-gray-600 leading-relaxed">
              Get pollution data specific to your neighborhood. Know exactly what you're breathing.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="glass-dark rounded-3xl p-8 card-hover">
            <div class="w-16 h-16 gradient-blue rounded-2xl flex items-center justify-center text-3xl mb-6">
              🤖
            </div>
            <h3 class="text-2xl font-bold mb-3">AI Predictions</h3>
            <p class="text-gray-600 leading-relaxed">
              Gemini AI predicts pollution spikes before they happen. Stay ahead of the curve.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="glass-dark rounded-3xl p-8 card-hover">
            <div class="w-16 h-16 bg-gradient-to-br from-green-400 to-emerald-600 rounded-2xl flex items-center justify-center text-3xl mb-6">
              🚨
            </div>
            <h3 class="text-2xl font-bold mb-3">Instant Alerts</h3>
            <p class="text-gray-600 leading-relaxed">
              Receive real-time notifications when air quality drops. Protect your health.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Dashboard Preview -->
    <div id="dashboard-preview" class="py-20 bg-gradient-to-br from-blue-50 to-purple-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16 fade-in">
          <h2 class="text-5xl font-bold mb-4">See it in action</h2>
          <p class="text-xl text-gray-600">Real-time data from Pavlodar sensors</p>
        </div>

        <div class="glass-dark rounded-3xl p-8 max-w-6xl mx-auto card-hover">
          <!-- Loading State -->
          <div v-if="loading" class="flex justify-center py-12">
            <div class="spinner"></div>
          </div>

          <!-- Current AQI -->
          <div v-else-if="currentAQI" class="text-center mb-8">
            <div class="inline-flex items-center space-x-4">
              <div
                class="w-24 h-24 rounded-full flex items-center justify-center text-3xl font-bold text-white shadow-2xl pulse-slow"
                :style="{ background: currentAQI.color }"
              >
                {{ currentAQI.aqi }}
              </div>
              <div class="text-left">
                <div class="text-sm text-gray-600">Current AQI</div>
                <div class="text-3xl font-bold">{{ currentAQI.category }}</div>
                <div class="text-sm text-gray-600">{{ currentAQI.dominant_pollutant }}</div>
              </div>
            </div>
          </div>

          <!-- Mini Stats Grid -->
          <div v-if="latestData" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div class="glass rounded-2xl p-4 text-center btn-hover">
              <div class="text-2xl mb-1">💨</div>
              <div class="text-xs text-gray-600">PM2.5</div>
              <div class="text-2xl font-bold">{{ latestData.pm25?.toFixed(1) || 'N/A' }}</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="glass rounded-2xl p-4 text-center btn-hover">
              <div class="text-2xl mb-1">🌫️</div>
              <div class="text-xs text-gray-600">PM10</div>
              <div class="text-2xl font-bold">{{ latestData.pm10?.toFixed(1) || 'N/A' }}</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="glass rounded-2xl p-4 text-center btn-hover">
              <div class="text-2xl mb-1">⚗️</div>
              <div class="text-xs text-gray-600">NO₂</div>
              <div class="text-2xl font-bold">{{ latestData.no2?.toFixed(1) || 'N/A' }}</div>
              <div class="text-xs text-gray-500">µg/m³</div>
            </div>
            <div class="glass rounded-2xl p-4 text-center btn-hover">
              <div class="text-2xl mb-1">🌡️</div>
              <div class="text-xs text-gray-600">Temp</div>
              <div class="text-2xl font-bold">{{ latestData.temperature?.toFixed(1) || 'N/A' }}°</div>
              <div class="text-xs text-gray-500">Celsius</div>
            </div>
          </div>

          <NuxtLink
            to="/dashboard"
            class="btn-hover w-full py-4 bg-black text-white rounded-2xl font-semibold text-center block"
          >
            View Full Dashboard →
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
      <div class="container mx-auto px-4 text-center text-white">
        <h2 class="text-5xl font-bold mb-6 fade-in">Ready to breathe easier?</h2>
        <p class="text-xl mb-8 opacity-90">Join the smart environmental monitoring revolution</p>
        <NuxtLink
          to="/register"
          class="btn-hover inline-block px-12 py-4 bg-white text-purple-600 rounded-full font-bold text-lg shadow-2xl"
        >
          Get Started Free
        </NuxtLink>
      </div>
    </div>

    <!-- Scrolling Text Banner -->
    <div class="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 py-8">
      <ScrollVelocity
        :texts="['ЕРТІС ЖАҒАСЫНДА', 'НА БЕРЕГУ ИРТЫША', 'BY THE IRTYSH RIVER']"
        :velocity="50"
        className="text-white"
        :numCopies="8"
      />
    </div>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="grid md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <div class="text-3xl">🌍</div>
              <div class="text-xl font-bold">EcoMonitor</div>
            </div>
            <p class="text-gray-400 text-sm">
              Making air quality data accessible to everyone in Pavlodar.
            </p>
          </div>
          <div>
            <h4 class="font-semibold mb-3">Product</h4>
            <div class="space-y-2 text-sm text-gray-400">
              <div class="hover:text-white cursor-pointer transition">Features</div>
              <div class="hover:text-white cursor-pointer transition">Pricing</div>
              <div class="hover:text-white cursor-pointer transition">API</div>
            </div>
          </div>
          <div>
            <h4 class="font-semibold mb-3">Company</h4>
            <div class="space-y-2 text-sm text-gray-400">
              <div class="hover:text-white cursor-pointer transition">About</div>
              <div class="hover:text-white cursor-pointer transition">Blog</div>
              <div class="hover:text-white cursor-pointer transition">Careers</div>
            </div>
          </div>
          <div>
            <h4 class="font-semibold mb-3">Resources</h4>
            <div class="space-y-2 text-sm text-gray-400">
              <div class="hover:text-white cursor-pointer transition">Documentation</div>
              <div class="hover:text-white cursor-pointer transition">Support</div>
              <div class="hover:text-white cursor-pointer transition">Status</div>
            </div>
          </div>
        </div>
        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>© 2025 EcoMonitor Pavlodar. Powered by Gemini AI • Made for GDG Fest Hackathon 2025</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()

const loading = ref(true)
const sensors = ref([])
const latestData = ref(null)
const currentAQI = ref(null)

// Scroll to dashboard preview
const scrollToDashboard = () => {
  document.getElementById('dashboard-preview')?.scrollIntoView({
    behavior: 'smooth'
  })
}

// Fetch preview data
const fetchPreviewData = async () => {
  loading.value = true
  try {
    // Fetch sensors count
    const sensorsRes = await fetch(`${config.public.iotApiUrl}/sensors`)
    const sensorsData = await sensorsRes.json()
    sensors.value = sensorsData.sensors || []

    // Fetch latest reading
    const readingsRes = await fetch(`${config.public.iotApiUrl}/readings/recent?limit=1`)
    const readingsData = await readingsRes.json()
    if (readingsData.readings && readingsData.readings.length > 0) {
      latestData.value = readingsData.readings[0]
    }

    // Fetch current AQI
    const aqiRes = await fetch(`${config.public.analyticsApiUrl}/aqi/current`)
    const aqiData = await aqiRes.json()
    currentAQI.value = aqiData
  } catch (error) {
    console.error('Error fetching preview data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPreviewData()
  // Auto-refresh every minute
  setInterval(fetchPreviewData, 60000)
})
</script>

<style scoped>
/* Blob animation */
@keyframes blob {
  0%, 100% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
