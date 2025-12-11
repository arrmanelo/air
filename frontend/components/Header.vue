<template>
  <header class="fixed top-0 left-0 right-0 z-40 glass-dark border-b border-white/10">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center space-x-3">
          <div class="text-3xl">🌍</div>
          <div>
            <h1 class="text-xl font-bold text-gradient">EcoMonitor</h1>
            <p class="text-xs text-gray-600">Smart Environmental Monitoring</p>
          </div>
        </NuxtLink>

        <!-- Navigation & Auth -->
        <div class="flex items-center space-x-4">
          <!-- Language Selector -->
          <div class="relative" ref="langMenu">
            <button
              @click="showLangMenu = !showLangMenu"
              class="flex items-center space-x-2 px-3 py-2 glass rounded-xl hover:bg-white/20 transition"
            >
              <span class="text-lg">{{ currentLangFlag }}</span>
              <span class="text-sm font-semibold">{{ currentLang }}</span>
              <span class="text-xs">▼</span>
            </button>

            <!-- Language Dropdown -->
            <transition name="fade">
              <div
                v-if="showLangMenu"
                class="absolute top-full mt-2 right-0 glass-dark rounded-xl shadow-xl overflow-hidden min-w-[150px]"
              >
                <button
                  v-for="lang in languages"
                  :key="lang.code"
                  @click="changeLang(lang.code)"
                  class="w-full flex items-center space-x-3 px-4 py-3 hover:bg-white/10 transition"
                  :class="{ 'bg-white/20': currentLang === lang.code }"
                >
                  <span class="text-lg">{{ lang.flag }}</span>
                  <span class="text-sm font-semibold">{{ lang.name }}</span>
                </button>
              </div>
            </transition>
          </div>

          <!-- User Profile (if logged in) -->
          <div v-if="user" class="relative" ref="profileMenu">
            <button
              @click="showProfileMenu = !showProfileMenu"
              class="flex items-center space-x-2 px-3 py-2 glass rounded-xl hover:bg-white/20 transition"
            >
              <img
                v-if="user.profile_picture"
                :src="user.profile_picture"
                :alt="user.name"
                class="w-8 h-8 rounded-full"
              />
              <div v-else class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold">
                {{ user.name.charAt(0).toUpperCase() }}
              </div>
              <span class="text-sm font-semibold hidden md:block">{{ user.name }}</span>
              <span class="text-xs">▼</span>
            </button>

            <!-- Profile Dropdown -->
            <transition name="fade">
              <div
                v-if="showProfileMenu"
                class="absolute top-full mt-2 right-0 glass-dark rounded-xl shadow-xl overflow-hidden min-w-[200px]"
              >
                <div class="px-4 py-3 border-b border-white/10">
                  <p class="text-sm font-semibold">{{ user.name }}</p>
                  <p class="text-xs text-gray-500">{{ user.email }}</p>
                </div>
                <NuxtLink
                  to="/dashboard"
                  class="flex items-center space-x-2 px-4 py-3 hover:bg-white/10 transition"
                >
                  <span>📊</span>
                  <span class="text-sm">{{ $t('nav.dashboard') }}</span>
                </NuxtLink>
                <button
                  @click="handleLogout"
                  class="w-full flex items-center space-x-2 px-4 py-3 hover:bg-white/10 transition text-red-500"
                >
                  <span>🚪</span>
                  <span class="text-sm">{{ $t('nav.logout') }}</span>
                </button>
              </div>
            </transition>
          </div>

          <!-- Login Button (if not logged in) -->
          <NuxtLink
            v-else
            to="/login"
            class="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold btn-hover glow"
          >
            {{ $t('nav.login') }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useI18n } from 'vue-i18n'

const auth = useAuth()
const { locale, t } = useI18n()

const user = computed(() => auth.user.value)
const showLangMenu = ref(false)
const showProfileMenu = ref(false)
const langMenu = ref(null)
const profileMenu = ref(null)

const languages = [
  { code: 'ru', name: 'Русский', flag: '🇷🇺' },
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'kz', name: 'Қазақша', flag: '🇰🇿' }
]

const currentLang = computed(() => locale.value.toUpperCase())
const currentLangFlag = computed(() => {
  return languages.find(l => l.code === locale.value)?.flag || '🌐'
})

const changeLang = (code) => {
  locale.value = code
  showLangMenu.value = false
  if (typeof window !== 'undefined') {
    localStorage.setItem('i18n_locale', code)
  }
}

const handleLogout = () => {
  auth.logout()
  showProfileMenu.value = false
}

// Close menus on click outside
const handleClickOutside = (event) => {
  if (langMenu.value && !langMenu.value.contains(event.target)) {
    showLangMenu.value = false
  }
  if (profileMenu.value && !profileMenu.value.contains(event.target)) {
    showProfileMenu.value = false
  }
}

onMounted(() => {
  auth.initAuth()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
