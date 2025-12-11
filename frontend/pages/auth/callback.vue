<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
    <div class="text-center">
      <div class="inline-block">
        <div class="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <p class="mt-4 text-lg text-gray-600">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '~/composables/useAuth'

const router = useRouter()
const route = useRoute()
const auth = useAuth()

const message = ref('Authenticating...')

onMounted(async () => {
  try {
    // Get token from URL query parameter
    const token = route.query.token

    if (!token) {
      message.value = 'Authentication failed: No token received'
      setTimeout(() => router.push('/login'), 2000)
      return
    }

    // Handle the callback
    const success = await auth.handleCallback(token)

    if (success) {
      message.value = 'Authentication successful! Redirecting...'
      setTimeout(() => router.push('/dashboard'), 1000)
    } else {
      message.value = 'Authentication failed. Redirecting to login...'
      setTimeout(() => router.push('/login'), 2000)
    }
  } catch (error) {
    console.error('Callback error:', error)
    message.value = 'An error occurred. Redirecting to login...'
    setTimeout(() => router.push('/login'), 2000)
  }
})
</script>
