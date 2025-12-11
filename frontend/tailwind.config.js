/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        'aqi-good': '#00e400',
        'aqi-moderate': '#ffff00',
        'aqi-unhealthy-sensitive': '#ff7e00',
        'aqi-unhealthy': '#ff0000',
        'aqi-very-unhealthy': '#8f3f97',
        'aqi-hazardous': '#7e0023',
      }
    },
  },
  plugins: [],
}
