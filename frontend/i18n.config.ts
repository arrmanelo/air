export default {
  locales: [
    {
      code: 'ru',
      name: 'Русский',
      file: 'ru.json'
    },
    {
      code: 'en',
      name: 'English',
      file: 'en.json'
    },
    {
      code: 'kz',
      name: 'Қазақша',
      file: 'kz.json'
    }
  ],
  defaultLocale: 'ru',
  strategy: 'no_prefix',
  detectBrowserLanguage: {
    useCookie: true,
    cookieKey: 'i18n_locale',
    alwaysRedirect: false,
    fallbackLocale: 'ru'
  }
}