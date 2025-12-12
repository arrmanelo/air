<template>
  <div class="min-h-screen bg-white">
    <!-- Hero Section -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-[#12ABAA]/5 via-white to-[#53BFBF]/5">
      <!-- Animated background circles -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-[#12ABAA]/10 rounded-full blur-3xl animate-float"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-[#FFC000]/10 rounded-full blur-3xl animate-float-delayed"></div>
      </div>

      <div class="container mx-auto px-4 py-20 relative z-10">
        <div class="max-w-6xl mx-auto">
          <!-- Main Title -->
          <div class="text-center mb-16 animate-fade-in">
            <h1 class="text-6xl md:text-8xl font-bold mb-6 text-gray-900">
              Качество воздуха,
              <span class="block mt-2 bg-gradient-to-r from-[#12ABAA] to-[#53BFBF] bg-clip-text text-transparent">
                под контролем AI
              </span>
            </h1>
            <p class="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto mb-12">
              Мониторинг окружающей среды в реальном времени. Отслеживайте уровень загрязнения, получайте мгновенные оповещения и дышите свободнее.
            </p>

            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button
                @click="scrollToMap"
                class="group px-8 py-4 bg-[#12ABAA] text-white rounded-2xl font-semibold text-lg shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300"
              >
                <span class="flex items-center gap-2">
                  Посмотреть карту
                  <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                  </svg>
                </span>
              </button>
              <NuxtLink
                to="/dashboard"
                class="px-8 py-4 border-2 border-[#12ABAA] text-[#12ABAA] rounded-2xl font-semibold text-lg hover:bg-[#12ABAA] hover:text-white transition-all duration-300"
              >
                Перейти к дашборду
              </NuxtLink>
            </div>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20">
            <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-[#12ABAA]">
              <div class="text-5xl font-bold bg-gradient-to-r from-[#12ABAA] to-[#53BFBF] bg-clip-text text-transparent mb-3">24/7</div>
              <div class="text-gray-600 font-medium">Мониторинг в реальном времени</div>
            </div>
            <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-[#FFC000]">
              <div class="text-5xl font-bold text-[#FFC000] mb-3">{{ sensors.length }}+</div>
              <div class="text-gray-600 font-medium">Активных датчиков</div>
            </div>
            <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-[#53BFBF]">
              <div class="text-5xl font-bold text-[#53BFBF] mb-3">AI</div>
              <div class="text-gray-600 font-medium">Аналитика на базе ИИ</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Current AQI Section -->
    <section v-if="currentAQI" class="py-20 bg-gradient-to-b from-white to-gray-50">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-4xl md:text-5xl font-bold text-center mb-12 text-gray-900">
            Текущее состояние воздуха
          </h2>

          <div class="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-gray-100">
            <div class="flex flex-col md:flex-row items-center justify-between gap-8">
              <!-- AQI Badge -->
              <div class="flex-shrink-0">
                <div
                  class="w-32 h-32 rounded-full flex items-center justify-center text-4xl font-bold text-white shadow-2xl animate-pulse-slow"
                  :style="{ backgroundColor: currentAQI.color }"
                >
                  {{ currentAQI.aqi }}
                </div>
              </div>

              <!-- AQI Info -->
              <div class="flex-1 text-center md:text-left">
                <div class="text-3xl font-bold text-gray-900 mb-2">{{ currentAQI.category }}</div>
                <div class="text-lg text-gray-600 mb-4">Основной загрязнитель: {{ currentAQI.dominant_pollutant }}</div>
                <div class="text-gray-500">{{ currentAQI.health_message }}</div>
              </div>
            </div>

            <!-- Pollutant Details -->
            <div v-if="latestData" class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 pt-8 border-t border-gray-100">
              <div class="bg-gradient-to-br from-[#12ABAA]/10 to-[#12ABAA]/5 rounded-2xl p-4 text-center">
                <div class="text-sm text-gray-600 mb-1">PM2.5</div>
                <div class="text-2xl font-bold text-[#12ABAA]">{{ latestData.pm25?.toFixed(1) || '-' }}</div>
                <div class="text-xs text-gray-500">мкг/м³</div>
              </div>
              <div class="bg-gradient-to-br from-[#53BFBF]/10 to-[#53BFBF]/5 rounded-2xl p-4 text-center">
                <div class="text-sm text-gray-600 mb-1">PM10</div>
                <div class="text-2xl font-bold text-[#53BFBF]">{{ latestData.pm10?.toFixed(1) || '-' }}</div>
                <div class="text-xs text-gray-500">мкг/м³</div>
              </div>
              <div class="bg-gradient-to-br from-[#FFC000]/10 to-[#FFC000]/5 rounded-2xl p-4 text-center">
                <div class="text-sm text-gray-600 mb-1">NO₂</div>
                <div class="text-2xl font-bold text-[#FFC000]">{{ latestData.no2?.toFixed(1) || '-' }}</div>
                <div class="text-xs text-gray-500">мкг/м³</div>
              </div>
              <div class="bg-gradient-to-br from-gray-400/10 to-gray-400/5 rounded-2xl p-4 text-center">
                <div class="text-sm text-gray-600 mb-1">Температура</div>
                <div class="text-2xl font-bold text-gray-700">{{ latestData.temperature?.toFixed(1) || '-' }}°</div>
                <div class="text-xs text-gray-500">Цельсия</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section -->
    <section id="map-section" class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-7xl mx-auto">
          <h2 class="text-4xl md:text-5xl font-bold text-center mb-4 text-gray-900">
            Карта датчиков Павлодара
          </h2>
          <p class="text-center text-gray-600 mb-12 text-lg">
            Интерактивная карта с данными в реальном времени
          </p>

          <div class="bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-100">
            <div class="h-[600px] relative">
              <ClientOnly>
                <MapView />
                <template #fallback>
                  <div class="absolute inset-0 flex items-center justify-center bg-gray-50">
                    <div class="flex flex-col items-center gap-4">
                      <div class="w-16 h-16 border-4 border-[#12ABAA] border-t-transparent rounded-full animate-spin"></div>
                      <div class="text-gray-600">Загрузка карты...</div>
                    </div>
                  </div>
                </template>
              </ClientOnly>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-gradient-to-b from-gray-50 to-white">
      <div class="container mx-auto px-4">
        <div class="max-w-6xl mx-auto">
          <h2 class="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
            Почему EcoMonitor?
          </h2>

          <div class="grid md:grid-cols-3 gap-8">
            <!-- Feature 1 -->
            <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-[#12ABAA]">
              <div class="w-16 h-16 bg-gradient-to-br from-[#12ABAA] to-[#53BFBF] rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
              <h3 class="text-2xl font-bold mb-3 text-gray-900">Гиперлокальные данные</h3>
              <p class="text-gray-600 leading-relaxed">
                Данные о загрязнении воздуха для каждого района. Знайте точно, чем вы дышите.
              </p>
            </div>

            <!-- Feature 2 -->
            <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-[#FFC000]">
              <div class="w-16 h-16 bg-gradient-to-br from-[#FFC000] to-[#FFC000]/70 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                </svg>
              </div>
              <h3 class="text-2xl font-bold mb-3 text-gray-900">AI-прогнозирование</h3>
              <p class="text-gray-600 leading-relaxed">
                Gemini AI предсказывает всплески загрязнений. Будьте на шаг впереди.
              </p>
            </div>

            <!-- Feature 3 -->
            <div class="group bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-[#53BFBF]">
              <div class="w-16 h-16 bg-gradient-to-br from-[#53BFBF] to-[#12ABAA] rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                </svg>
              </div>
              <h3 class="text-2xl font-bold mb-3 text-gray-900">Мгновенные оповещения</h3>
              <p class="text-gray-600 leading-relaxed">
                Получайте уведомления в реальном времени, когда качество воздуха ухудшается.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Scroll Velocity Section -->
    <div class="bg-gradient-to-r from-[#12ABAA] via-[#53BFBF] to-[#12ABAA] py-16 overflow-hidden">
      <ScrollVelocity
        :texts="['Чистый воздух для всех', 'Мониторинг 24/7', 'Аналитика на базе ИИ', 'Дышите свободнее']"
        :velocity="scrollVelocity"
        className="text-white"
      />
    </div>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="max-w-6xl mx-auto">
          <div class="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div class="flex items-center gap-3 mb-4">
                <div class="text-3xl">🌍</div>
                <div class="text-xl font-bold">EcoMonitor</div>
              </div>
              <p class="text-gray-400 text-sm">
                Делаем данные о качестве воздуха доступными для всех в Павлодаре.
              </p>
            </div>
            <div>
              <h4 class="font-semibold mb-3">Продукт</h4>
              <div class="space-y-2 text-sm text-gray-400">
                <div class="hover:text-white cursor-pointer transition">Функции</div>
                <div class="hover:text-white cursor-pointer transition">Цены</div>
                <div class="hover:text-white cursor-pointer transition">API</div>
              </div>
            </div>
            <div>
              <h4 class="font-semibold mb-3">Компания</h4>
              <div class="space-y-2 text-sm text-gray-400">
                <div class="hover:text-white cursor-pointer transition">О нас</div>
                <div class="hover:text-white cursor-pointer transition">Блог</div>
                <div class="hover:text-white cursor-pointer transition">Карьера</div>
              </div>
            </div>
            <div>
              <h4 class="font-semibold mb-3">Ресурсы</h4>
              <div class="space-y-2 text-sm text-gray-400">
                <div class="hover:text-white cursor-pointer transition">Документация</div>
                <div class="hover:text-white cursor-pointer transition">Поддержка</div>
                <div class="hover:text-white cursor-pointer transition">Статус</div>
              </div>
            </div>
          </div>
          <div class="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
            <p>© 2025 EcoMonitor Павлодар. На базе Gemini AI • Создано для GDG Fest Hackathon 2025</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ScrollVelocity from '~/components/ScrollVelocity.vue'

const config = useRuntimeConfig()

const loading = ref(true)
const sensors = ref([])
const latestData = ref(null)
const currentAQI = ref(null)
const scrollVelocity = ref(5)

const scrollToMap = () => {
  document.getElementById('map-section')?.scrollIntoView({
    behavior: 'smooth'
  })
}

const fetchPreviewData = async () => {
  loading.value = true
  try {
    // Fetch sensors
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
    console.error('Ошибка загрузки данных:', error)
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
@keyframes float {
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

@keyframes float-delayed {
  0%, 100% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(-30px, 50px) scale(0.9);
  }
  66% {
    transform: translate(20px, -20px) scale(1.1);
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse-slow {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.animate-float {
  animation: float 20s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float-delayed 25s ease-in-out infinite;
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}

.animate-pulse-slow {
  animation: pulse-slow 3s ease-in-out infinite;
}
</style>
