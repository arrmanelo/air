// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  modules: ['@nuxtjs/tailwindcss', '@nuxtjs/i18n'],

  i18n: {
    locales: [
      { code: 'ru', name: 'Русский', file: 'ru.json' },
      { code: 'en', name: 'English', file: 'en.json' },
      { code: 'kz', name: 'Қазақша', file: 'kz.json' }
    ],
    lazy: true,

    // ТВОЯ ПРАВИЛЬНАЯ ПАПКА — "locales/"
    // Именно она есть в проекте (см. твой скрин), поэтому ставим:
    langDir: 'locales/',

    defaultLocale: 'ru',
    strategy: 'no_prefix',

    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_locale',
      alwaysRedirect: false,
      fallbackLocale: 'ru'
    }
  },

  runtimeConfig: {
    public: {
      authApiUrl: process.env.NUXT_PUBLIC_AUTH_API_URL || 'http://localhost:8004',
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
