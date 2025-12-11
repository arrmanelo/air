<template>
  <div class="fixed bottom-6 right-6 z-50">
    <!-- Chat Window -->
    <transition name="chat-slide">
      <div
        v-if="isOpen"
        class="glass-dark rounded-3xl shadow-2xl mb-4 w-96 max-h-[600px] flex flex-col overflow-hidden fade-in"
      >
        <!-- Header -->
        <div class="bg-gradient-to-r from-green-500 to-blue-600 p-4 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
              <span class="text-2xl">🤖</span>
            </div>
            <div>
              <h3 class="text-white font-bold">EcoGuide</h3>
              <p class="text-white/80 text-xs">Виртуальный эко-ассистент</p>
            </div>
          </div>
          <button
            @click="isOpen = false"
            class="text-white/80 hover:text-white transition"
          >
            ✕
          </button>
        </div>

        <!-- Messages -->
        <div
          ref="messagesContainer"
          class="flex-1 overflow-y-auto p-4 space-y-4 bg-white/50"
        >
          <!-- Welcome Message -->
          <div v-if="messages.length === 0" class="text-center py-8">
            <div class="text-6xl mb-4">🌍</div>
            <h4 class="text-lg font-semibold mb-2">Привет! Я EcoGuide</h4>
            <p class="text-sm text-gray-600 mb-4">
              Спроси меня о качестве воздуха в твоем районе!
            </p>

            <!-- Suggestions -->
            <div class="space-y-2">
              <p class="text-xs text-gray-500 font-semibold mb-2">Примеры вопросов:</p>
              <button
                v-for="(suggestion, idx) in suggestions"
                :key="idx"
                @click="sendMessage(suggestion)"
                class="block w-full text-left px-3 py-2 glass rounded-xl text-sm hover:bg-white/50 transition"
              >
                {{ suggestion }}
              </button>
            </div>
          </div>

          <!-- Chat Messages -->
          <div
            v-for="(msg, idx) in messages"
            :key="idx"
            :class="[
              'flex',
              msg.type === 'user' ? 'justify-end' : 'justify-start'
            ]"
          >
            <div
              :class="[
                'max-w-[80%] rounded-2xl px-4 py-2',
                msg.type === 'user'
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                  : 'glass border border-gray-200'
              ]"
            >
              <p class="text-sm whitespace-pre-wrap">{{ msg.text }}</p>

              <!-- Data card for assistant messages -->
              <div
                v-if="msg.type === 'assistant' && msg.data"
                class="mt-3 p-3 bg-white/50 rounded-xl text-xs space-y-1"
              >
                <div class="flex items-center justify-between">
                  <span class="font-semibold">AQI:</span>
                  <span
                    class="px-2 py-1 rounded-full text-white font-bold"
                    :style="{ backgroundColor: getAQIColor(msg.data.aqi) }"
                  >
                    {{ msg.data.aqi }}
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">PM2.5:</span>
                  <span class="font-semibold">{{ msg.data.pm25?.toFixed(1) || 'н/д' }} µg/m³</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Температура:</span>
                  <span class="font-semibold">{{ msg.data.temperature?.toFixed(1) || 'н/д' }}°C</span>
                </div>
              </div>

              <!-- Recommendations -->
              <div
                v-if="msg.type === 'assistant' && msg.recommendations && msg.recommendations.length > 0"
                class="mt-3 space-y-1"
              >
                <p class="text-xs font-semibold mb-1">Рекомендации:</p>
                <div
                  v-for="(rec, ridx) in msg.recommendations.slice(0, 3)"
                  :key="ridx"
                  class="text-xs bg-white/30 rounded-lg px-2 py-1"
                >
                  {{ rec }}
                </div>
              </div>

              <p class="text-xs opacity-70 mt-2">{{ msg.time }}</p>
            </div>
          </div>

          <!-- Typing indicator -->
          <div v-if="isTyping" class="flex justify-start">
            <div class="glass border border-gray-200 rounded-2xl px-4 py-3">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input -->
        <form @submit.prevent="handleSend" class="p-4 bg-white/80 border-t border-gray-200">
          <div class="flex space-x-2">
            <input
              v-model="inputMessage"
              type="text"
              placeholder="Спросите о качестве воздуха..."
              class="flex-1 px-4 py-3 glass border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              :disabled="isTyping"
            />
            <button
              type="submit"
              :disabled="!inputMessage.trim() || isTyping"
              class="px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed btn-hover glow"
            >
              📤
            </button>
          </div>
        </form>
      </div>
    </transition>

    <!-- Floating Button -->
    <button
      @click="toggleChat"
      class="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-600 rounded-full shadow-2xl flex items-center justify-center btn-hover glow pulse-slow"
    >
      <span v-if="!isOpen" class="text-3xl">🤖</span>
      <span v-else class="text-2xl text-white">✕</span>
    </button>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const API_URL = 'http://localhost:8005'

const isOpen = ref(false)
const inputMessage = ref('')
const messages = ref([])
const isTyping = ref(false)
const messagesContainer = ref(null)

const suggestions = ref([
  'Какой сейчас воздух на улице Лермонтова?',
  'Можно ли гулять сегодня?',
  'Безопасно ли бегать утром?',
  'Стоит ли открывать окна?'
])

const toggleChat = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && messages.value.length === 0) {
    loadSuggestions()
  }
}

const loadSuggestions = async () => {
  try {
    const response = await fetch(`${API_URL}/suggestions`)
    const data = await response.json()
    suggestions.value = data.suggestions || suggestions.value
  } catch (error) {
    console.error('Failed to load suggestions:', error)
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const getAQIColor = (aqi) => {
  if (aqi <= 50) return '#00e400'
  if (aqi <= 100) return '#ffff00'
  if (aqi <= 150) return '#ff7e00'
  if (aqi <= 200) return '#ff0000'
  if (aqi <= 300) return '#8f3f97'
  return '#7e0023'
}

const sendMessage = async (text) => {
  if (!text || !text.trim()) return

  const userMessage = {
    type: 'user',
    text: text,
    time: new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  }

  messages.value.push(userMessage)
  inputMessage.value = ''
  scrollToBottom()

  // Get user location (optional)
  let location = null
  try {
    if (navigator.geolocation) {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject)
      })
      location = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      }
    }
  } catch (error) {
    console.log('Location not available')
  }

  // Call AI assistant
  isTyping.value = true

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: text,
        latitude: location?.latitude,
        longitude: location?.longitude
      })
    })

    const data = await response.json()

    const assistantMessage = {
      type: 'assistant',
      text: data.response,
      data: data.data,
      recommendations: data.recommendations,
      time: new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    }

    messages.value.push(assistantMessage)
  } catch (error) {
    console.error('Chat error:', error)
    messages.value.push({
      type: 'assistant',
      text: '😔 Извините, произошла ошибка. Попробуйте еще раз.',
      time: new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    })
  } finally {
    isTyping.value = false
    scrollToBottom()
  }
}

const handleSend = () => {
  sendMessage(inputMessage.value)
}
</script>

<style scoped>
.chat-slide-enter-active,
.chat-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-slide-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.chat-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
</style>
