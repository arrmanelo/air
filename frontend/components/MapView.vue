<template>
  <div ref="mapContainer" class="w-full h-full"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  sensors: {
    type: Array,
    default: () => []
  },
  latestReadings: {
    type: Array,
    default: () => []
  }
})

const mapContainer = ref(null)
let map = null
let markers = []
let L = null

// Initialize map
onMounted(async () => {
  if (process.client) {
    // Динамический импорт Leaflet только на клиенте
    L = (await import('leaflet')).default

    // Pavlodar coordinates
    const pavlodarCoords = [52.2873, 76.9674]

    map = L.map(mapContainer.value).setView(pavlodarCoords, 12)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map)

    // Add markers
    updateMarkers()
  }
})

// Update markers when sensors change
watch(() => props.sensors, () => {
  updateMarkers()
}, { deep: true })

const updateMarkers = () => {
  if (!map || !L) return

  // Clear existing markers
  markers.forEach(marker => marker.remove())
  markers = []

  // Add sensor markers
  props.sensors.forEach(sensor => {
    const reading = props.latestReadings.find(r => r.sensor_id === sensor.sensor_id)

    // Determine marker color based on PM2.5 level
    let markerColor = '#12ABAA'
    if (reading?.pm25) {
      if (reading.pm25 > 150) markerColor = '#ef4444'
      else if (reading.pm25 > 55) markerColor = '#FFC000'
      else if (reading.pm25 > 35) markerColor = '#f59e0b'
    }

    const icon = L.divIcon({
      className: 'custom-marker',
      html: `
        <div style="
          background-color: ${markerColor};
          width: 32px;
          height: 32px;
          border-radius: 50%;
          border: 3px solid white;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          color: white;
          font-size: 11px;
        ">
          ${reading?.pm25?.toFixed(0) || '?'}
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    })

    const marker = L.marker([sensor.latitude, sensor.longitude], { icon })
      .addTo(map)
      .bindPopup(`
        <div style="min-width: 220px; font-family: system-ui, sans-serif;">
          <h3 style="font-weight: 700; margin-bottom: 8px; color: #12ABAA; font-size: 16px;">${sensor.name}</h3>
          <p style="font-size: 13px; color: #666; margin-bottom: 12px;">${sensor.location_description}</p>
          ${reading ? `
            <div style="font-size: 14px;">
              <div style="margin-bottom: 6px; padding: 6px; background: #f3f4f6; border-radius: 6px;">
                <strong style="color: #12ABAA;">PM2.5:</strong> ${reading.pm25?.toFixed(1) || 'N/A'} <span style="color: #666;">мкг/м³</span>
              </div>
              <div style="margin-bottom: 6px; padding: 6px; background: #f3f4f6; border-radius: 6px;">
                <strong style="color: #53BFBF;">PM10:</strong> ${reading.pm10?.toFixed(1) || 'N/A'} <span style="color: #666;">мкг/м³</span>
              </div>
              <div style="margin-bottom: 6px; padding: 6px; background: #f3f4f6; border-radius: 6px;">
                <strong style="color: #FFC000;">NO₂:</strong> ${reading.no2?.toFixed(1) || 'N/A'} <span style="color: #666;">мкг/м³</span>
              </div>
              <div style="padding: 6px; background: #f3f4f6; border-radius: 6px;">
                <strong style="color: #6b7280;">Температура:</strong> ${reading.temperature?.toFixed(1) || 'N/A'} <span style="color: #666;">°C</span>
              </div>
            </div>
          ` : '<p style="color: #999; text-align: center; padding: 12px;">Нет данных</p>'}
        </div>
      `)

    markers.push(marker)
  })
}
</script>

<style scoped>
/* Map marker styles are inline */
</style>
