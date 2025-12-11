// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  modules: ['@nuxtjs/tailwindcss'],

  runtimeConfig: {
    public: {
      // Firebase
      firebaseApiKey: process.env.NUXT_PUBLIC_FIREBASE_API_KEY,
      firebaseAuthDomain: process.env.NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
      firebaseProjectId: process.env.NUXT_PUBLIC_FIREBASE_PROJECT_ID,
      firebaseStorageBucket: process.env.NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
      firebaseMessagingSenderId: process.env.NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
      firebaseAppId: process.env.NUXT_PUBLIC_FIREBASE_APP_ID,

      // API Endpoints
      iotApiUrl: process.env.NUXT_PUBLIC_IOT_API_URL || 'http://localhost:8001',
      analyticsApiUrl: process.env.NUXT_PUBLIC_ANALYTICS_API_URL || 'http://localhost:8002',
      alertApiUrl: process.env.NUXT_PUBLIC_ALERT_API_URL || 'http://localhost:8003'
    }
  },

  app: {
    head: {
      title: 'EcoMonitor Pavlodar - Smart Environmental Monitoring',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { hid: 'description', name: 'description', content: 'Real-time environmental monitoring for Pavlodar, Kazakhstan' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'stylesheet', href: 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css' }
      ]
    }
  },

  css: ['~/assets/css/main.css']
})
