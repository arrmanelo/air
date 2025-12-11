<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
    <!-- Animated Background Blobs -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
      <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-20 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Login Card -->
    <div class="relative z-10 w-full max-w-md">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center justify-center space-x-3 mb-8">
        <div class="text-5xl">🌍</div>
        <div>
          <h1 class="text-3xl font-bold text-gradient">EcoMonitor</h1>
          <p class="text-sm text-gray-600">Smart Environmental Monitoring</p>
        </div>
      </NuxtLink>

      <!-- Login Form -->
      <div class="glass-dark rounded-3xl p-8 card-hover fade-in">
        <h2 class="text-2xl font-bold mb-2">Welcome back</h2>
        <p class="text-gray-600 mb-6">Sign in to access your dashboard</p>

        <!-- Error Message -->
        <div v-if="errorMessage" class="glass border border-red-200 rounded-2xl p-4 mb-6 bg-red-50/50">
          <div class="flex items-start space-x-2">
            <span class="text-xl">⚠️</span>
            <p class="text-sm text-red-600">{{ errorMessage }}</p>
          </div>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Email Input -->
          <div>
            <label for="email" class="block text-sm font-semibold mb-2">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              placeholder="your@email.com"
              class="w-full px-4 py-3 glass border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>

          <!-- Password Input -->
          <div>
            <label for="password" class="block text-sm font-semibold mb-2">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 glass border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>

          <!-- Remember Me -->
          <div class="flex items-center justify-between">
            <label class="flex items-center space-x-2 cursor-pointer">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span class="text-sm text-gray-600">Remember me</span>
            </label>
            <a href="#" class="text-sm text-blue-600 hover:text-blue-700 transition">
              Forgot password?
            </a>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-hover py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl font-semibold text-lg glow disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">Sign In →</span>
            <span v-else class="flex items-center justify-center">
              <div class="spinner-small mr-2"></div>
              Signing in...
            </span>
          </button>
        </form>

        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 glass text-gray-600">Or continue with</span>
          </div>
        </div>

        <!-- Social Login Buttons -->
        <div class="mb-6">
          <button
            @click="handleGoogleLogin"
            class="w-full btn-hover py-3 glass border border-gray-200 rounded-2xl font-semibold flex items-center justify-center space-x-2"
          >
            <span>🔍</span>
            <span>Continue with Google</span>
          </button>
        </div>

        <!-- Sign Up Link -->
        <div class="text-center text-sm text-gray-600">
          Don't have an account?
          <NuxtLink to="/register" class="text-blue-600 hover:text-blue-700 font-semibold transition">
            Sign up
          </NuxtLink>
        </div>
      </div>

      <!-- Back to Home -->
      <div class="text-center mt-6">
        <NuxtLink to="/" class="text-sm text-gray-600 hover:text-gray-900 transition">
          ← Back to home
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '~/composables/useAuth'

const router = useRouter()
const auth = useAuth()

// State
const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const loading = ref(false)
const errorMessage = ref('')

// Check if already authenticated
onMounted(async () => {
  auth.initAuth()
  if (auth.isAuthenticated.value) {
    router.push('/dashboard')
  }
})

// Handle email/password login (disabled for now, using Google OAuth only)
const handleLogin = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    // For now, redirect to Google login
    errorMessage.value = 'Please use Google Sign-In to continue'
    loading.value = false
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = error.message || 'Invalid email or password. Please try again.'
  } finally {
    loading.value = false
  }
}

// Handle Google login
const handleGoogleLogin = () => {
  auth.loginWithGoogle()
}

// Load remembered email
if (typeof window !== 'undefined') {
  const rememberedEmail = localStorage.getItem('userEmail')
  if (rememberedEmail) {
    email.value = rememberedEmail
    rememberMe.value = true
  }
}
</script>

<style scoped>
.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
