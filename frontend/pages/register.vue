<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
    <!-- Animated Background Blobs -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
      <div class="absolute top-40 right-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-20 w-72 h-72 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Register Card -->
    <div class="relative z-10 w-full max-w-md">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center justify-center space-x-3 mb-8">
        <div class="text-5xl">🌍</div>
        <div>
          <h1 class="text-3xl font-bold text-gradient">EcoMonitor</h1>
          <p class="text-sm text-gray-600">Smart Environmental Monitoring</p>
        </div>
      </NuxtLink>

      <!-- Register Form -->
      <div class="glass-dark rounded-3xl p-8 card-hover fade-in">
        <h2 class="text-2xl font-bold mb-2">Create your account</h2>
        <p class="text-gray-600 mb-6">Start monitoring air quality in Pavlodar</p>

        <!-- Error Message -->
        <div v-if="errorMessage" class="glass border border-red-200 rounded-2xl p-4 mb-6 bg-red-50/50">
          <div class="flex items-start space-x-2">
            <span class="text-xl">⚠️</span>
            <p class="text-sm text-red-600">{{ errorMessage }}</p>
          </div>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="glass border border-green-200 rounded-2xl p-4 mb-6 bg-green-50/50">
          <div class="flex items-start space-x-2">
            <span class="text-xl">✅</span>
            <p class="text-sm text-green-600">{{ successMessage }}</p>
          </div>
        </div>

        <!-- Register Form -->
        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Full Name Input -->
          <div>
            <label for="fullName" class="block text-sm font-semibold mb-2">Full Name</label>
            <input
              id="fullName"
              v-model="fullName"
              type="text"
              required
              placeholder="John Doe"
              class="w-full px-4 py-3 glass border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>

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
            <p class="text-xs text-gray-500 mt-1">Must be at least 6 characters</p>
          </div>

          <!-- Confirm Password Input -->
          <div>
            <label for="confirmPassword" class="block text-sm font-semibold mb-2">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 glass border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>

          <!-- Terms Checkbox -->
          <div>
            <label class="flex items-start space-x-2 cursor-pointer">
              <input
                v-model="agreeToTerms"
                type="checkbox"
                required
                class="mt-1 w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span class="text-sm text-gray-600">
                I agree to the
                <a href="#" class="text-blue-600 hover:text-blue-700">Terms of Service</a>
                and
                <a href="#" class="text-blue-600 hover:text-blue-700">Privacy Policy</a>
              </span>
            </label>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-hover py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl font-semibold text-lg glow disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">Create Account →</span>
            <span v-else class="flex items-center justify-center">
              <div class="spinner-small mr-2"></div>
              Creating account...
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
        <div class="grid grid-cols-2 gap-4 mb-6">
          <button
            @click="handleGoogleSignup"
            class="btn-hover py-3 glass border border-gray-200 rounded-2xl font-semibold flex items-center justify-center space-x-2"
          >
            <span>🔍</span>
            <span>Google</span>
          </button>
          <button
            @click="handleGithubSignup"
            class="btn-hover py-3 glass border border-gray-200 rounded-2xl font-semibold flex items-center justify-center space-x-2"
          >
            <span>⚫</span>
            <span>GitHub</span>
          </button>
        </div>

        <!-- Sign In Link -->
        <div class="text-center text-sm text-gray-600">
          Already have an account?
          <NuxtLink to="/login" class="text-blue-600 hover:text-blue-700 font-semibold transition">
            Sign in
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// State
const fullName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const agreeToTerms = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Firebase auth instance
let auth = null

// Initialize Firebase Auth
const initFirebase = async () => {
  try {
    const { getAuth, createUserWithEmailAndPassword, updateProfile, signInWithPopup, GoogleAuthProvider, GithubAuthProvider } = await import('firebase/auth')
    const { initializeApp, getApps } = await import('firebase/app')

    const config = useRuntimeConfig()

    // Initialize Firebase if not already initialized
    if (getApps().length === 0) {
      const firebaseConfig = {
        apiKey: config.public.firebaseApiKey,
        authDomain: config.public.firebaseAuthDomain,
        projectId: config.public.firebaseProjectId,
        storageBucket: config.public.firebaseStorageBucket,
        messagingSenderId: config.public.firebaseMessagingSenderId,
        appId: config.public.firebaseAppId
      }
      initializeApp(firebaseConfig)
    }

    auth = getAuth()
    return true
  } catch (error) {
    console.error('Firebase not available:', error)
    return false
  }
}

// Handle registration
const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  // Validate passwords match
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match'
    return
  }

  // Validate password length
  if (password.value.length < 6) {
    errorMessage.value = 'Password must be at least 6 characters'
    return
  }

  loading.value = true

  try {
    // Initialize Firebase
    const firebaseAvailable = await initFirebase()

    if (!firebaseAvailable) {
      // Fallback: Direct navigation without authentication
      console.warn('Firebase not configured, skipping authentication')
      successMessage.value = 'Account created! Redirecting...'
      setTimeout(() => router.push('/dashboard'), 1500)
      return
    }

    const { createUserWithEmailAndPassword, updateProfile } = await import('firebase/auth')

    // Create user with Firebase
    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value)
    const user = userCredential.user

    // Update profile with display name
    await updateProfile(user, {
      displayName: fullName.value
    })

    // Get ID token
    const idToken = await user.getIdToken()

    // Store token
    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', idToken)
    }

    // Show success message
    successMessage.value = 'Account created successfully! Redirecting...'

    // Redirect to dashboard after a short delay
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  } catch (error) {
    console.error('Registration error:', error)
    if (error.code === 'auth/email-already-in-use') {
      errorMessage.value = 'This email is already registered. Please sign in instead.'
    } else if (error.code === 'auth/weak-password') {
      errorMessage.value = 'Password is too weak. Please choose a stronger password.'
    } else if (error.code === 'auth/invalid-email') {
      errorMessage.value = 'Invalid email address.'
    } else {
      errorMessage.value = error.message || 'Registration failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Handle Google signup
const handleGoogleSignup = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    const firebaseAvailable = await initFirebase()
    if (!firebaseAvailable) {
      errorMessage.value = 'Google Sign-Up requires Firebase configuration'
      loading.value = false
      return
    }

    const { signInWithPopup, GoogleAuthProvider } = await import('firebase/auth')
    const provider = new GoogleAuthProvider()

    const result = await signInWithPopup(auth, provider)
    const user = result.user
    const idToken = await user.getIdToken()

    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', idToken)
    }

    successMessage.value = 'Account created successfully! Redirecting...'
    setTimeout(() => router.push('/dashboard'), 1500)
  } catch (error) {
    console.error('Google signup error:', error)
    errorMessage.value = error.message || 'Google Sign-Up failed. Please try again.'
  } finally {
    loading.value = false
  }
}

// Handle GitHub signup
const handleGithubSignup = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    const firebaseAvailable = await initFirebase()
    if (!firebaseAvailable) {
      errorMessage.value = 'GitHub Sign-Up requires Firebase configuration'
      loading.value = false
      return
    }

    const { signInWithPopup, GithubAuthProvider } = await import('firebase/auth')
    const provider = new GithubAuthProvider()

    const result = await signInWithPopup(auth, provider)
    const user = result.user
    const idToken = await user.getIdToken()

    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', idToken)
    }

    successMessage.value = 'Account created successfully! Redirecting...'
    setTimeout(() => router.push('/dashboard'), 1500)
  } catch (error) {
    console.error('GitHub signup error:', error)
    errorMessage.value = error.message || 'GitHub Sign-Up failed. Please try again.'
  } finally {
    loading.value = false
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
