/**
 * Authentication composable for managing user auth state
 */
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const API_URL = typeof window !== 'undefined'
  ? (window.location.hostname === 'localhost' ? 'http://localhost:8004' : 'https://api.weimea.com')
  : 'http://localhost:8004'

interface User {
  id: number
  email: string
  name: string
  profile_picture?: string
  role: string
}

const user = ref<User | null>(null)
const token = ref<string | null>(null)
const loading = ref(false)

export const useAuth = () => {
  const router = useRouter()

  // Initialize auth state from localStorage
  const initAuth = () => {
    if (typeof window === 'undefined') return

    const storedToken = localStorage.getItem('authToken')
    if (storedToken) {
      token.value = storedToken
      // Verify token and load user
      verifyToken()
    }
  }

  // Verify JWT token
  const verifyToken = async () => {
    if (!token.value) return false

    try {
      const response = await fetch(`${API_URL}/auth/verify`, {
        headers: {
          'Authorization': `Bearer ${token.value}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        user.value = data.user
        return true
      } else {
        // Token invalid, clear it
        logout()
        return false
      }
    } catch (error) {
      console.error('Token verification failed:', error)
      logout()
      return false
    }
  }

  // Get current user
  const getCurrentUser = async () => {
    if (!token.value) return null

    try {
      const response = await fetch(`${API_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token.value}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        user.value = data
        return data
      }
      return null
    } catch (error) {
      console.error('Failed to get user:', error)
      return null
    }
  }

  // Login with Google
  const loginWithGoogle = () => {
    // Redirect to backend Google OAuth
    window.location.href = `${API_URL}/auth/google/login`
  }

  // Handle OAuth callback (called from auth/callback page)
  const handleCallback = async (callbackToken: string) => {
    if (!callbackToken) return false

    token.value = callbackToken

    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', callbackToken)
    }

    // Verify token and load user
    const valid = await verifyToken()
    return valid
  }

  // Logout
  const logout = () => {
    token.value = null
    user.value = null

    if (typeof window !== 'undefined') {
      localStorage.removeItem('authToken')
      localStorage.removeItem('userEmail')
    }

    router.push('/login')
  }

  // Check if user is authenticated
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  return {
    user,
    token,
    loading,
    isAuthenticated,
    initAuth,
    verifyToken,
    getCurrentUser,
    loginWithGoogle,
    handleCallback,
    logout,
  }
}
