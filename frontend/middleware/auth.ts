/**
 * Authentication middleware to protect routes
 */
export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware on server-side
  if (process.server) return

  const { useAuth } = await import('~/composables/useAuth')
  const auth = useAuth()

  // Initialize auth state
  auth.initAuth()

  // If trying to access protected route without auth, redirect to login
  const protectedRoutes = ['/dashboard']
  const isProtectedRoute = protectedRoutes.some(route => to.path.startsWith(route))

  if (isProtectedRoute && !auth.token.value) {
    return navigateTo('/login')
  }

  // If authenticated and trying to access auth pages, redirect to dashboard
  const authPages = ['/login', '/register']
  const isAuthPage = authPages.includes(to.path)

  if (isAuthPage && auth.token.value) {
    return navigateTo('/dashboard')
  }
})
