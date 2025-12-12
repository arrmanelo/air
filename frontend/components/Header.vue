<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-100">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center gap-3 group">
          <div class="text-3xl transition-transform group-hover:scale-110">🌍</div>
          <div>
            <h1 class="text-xl font-bold bg-gradient-to-r from-[#12ABAA] to-[#53BFBF] bg-clip-text text-transparent">
              EcoMonitor
            </h1>
            <p class="text-xs text-gray-500">Умный мониторинг</p>
          </div>
        </NuxtLink>

        <!-- Navigation & Auth -->
        <div class="flex items-center gap-4">
          <!-- User Profile (if logged in) -->
          <div v-if="user" class="relative" ref="profileMenu">
            <button
              @click="showProfileMenu = !showProfileMenu"
              class="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-[#12ABAA] to-[#53BFBF] text-white hover:shadow-lg transition-all duration-300"
            >
              <img
                v-if="user.profile_picture"
                :src="user.profile_picture"
                :alt="user.name"
                class="w-8 h-8 rounded-full border-2 border-white"
              />
              <div v-else class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-white font-bold">
                {{ user.name.charAt(0).toUpperCase() }}
              </div>
              <span class="text-sm font-semibold hidden md:block">{{ user.name }}</span>
              <svg class="w-4 h-4" :class="{ 'rotate-180': showProfileMenu }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>

            <!-- Profile Dropdown -->
            <transition name="dropdown">
              <div
                v-if="showProfileMenu"
                class="absolute top-full mt-2 right-0 bg-white rounded-2xl shadow-2xl overflow-hidden min-w-[220px] border border-gray-100"
              >
                <div class="px-4 py-3 bg-gradient-to-r from-[#12ABAA]/5 to-[#53BFBF]/5 border-b border-gray-100">
                  <p class="text-sm font-semibold text-gray-900">{{ user.name }}</p>
                  <p class="text-xs text-gray-500">{{ user.email }}</p>
                </div>
                <NuxtLink
                  to="/dashboard"
                  class="flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition-colors"
                  @click="showProfileMenu = false"
                >
                  <div class="w-8 h-8 rounded-lg bg-[#12ABAA]/10 flex items-center justify-center">
                    <svg class="w-4 h-4 text-[#12ABAA]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-gray-700">Дашборд</span>
                </NuxtLink>
                <button
                  @click="handleLogout"
                  class="w-full flex items-center gap-3 px-4 py-3 hover:bg-red-50 transition-colors text-red-600"
                >
                  <div class="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center">
                    <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                    </svg>
                  </div>
                  <span class="text-sm font-medium">Выход</span>
                </button>
              </div>
            </transition>
          </div>

          <!-- Login Button (if not logged in) -->
          <NuxtLink
            v-else
            to="/login"
            class="px-6 py-2.5 bg-gradient-to-r from-[#12ABAA] to-[#53BFBF] text-white rounded-xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300"
          >
            Войти
          </NuxtLink>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useAuth } from '~/composables/useAuth'

const auth = useAuth()

const user = computed(() => auth.user.value)
const showProfileMenu = ref(false)
const profileMenu = ref(null)

const handleLogout = () => {
  auth.logout()
  showProfileMenu.value = false
}

// Close menu on click outside
const handleClickOutside = (event) => {
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
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
}
</style>
