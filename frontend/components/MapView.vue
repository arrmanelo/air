<template>
  <div ref="mapContainer" class="w-full h-full"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import L from 'leaflet'

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

// Initialize map
onMounted(() => {
  if (process.client) {
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
  if (!map) return

  // Clear existing markers
  markers.forEach(marker => marker.remove())
  markers = []

  // Add sensor markers
  props.sensors.forEach(sensor => {
    const reading = props.latestReadings.find(r => r.sensor_id === sensor.sensor_id)

    // Determine marker color based on PM2.5 level
    let markerColor = 'green'
    if (reading?.pm25) {
      if (reading.pm25 > 150) markerColor = 'red'
      else if (reading.pm25 > 55) markerColor = 'orange'
      else if (reading.pm25 > 35) markerColor = 'yellow'
    }

    const icon = L.divIcon({
      className: 'custom-marker',
      html: `
        <div style="
          background-color: ${markerColor};
          width: 30px;
          height: 30px;
          border-radius: 50%;
          border: 3px solid white;
          box-shadow: 0 2px 5px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          color: white;
          font-size: 10px;
        ">
          ${reading?.pm25?.toFixed(0) || '?'}
        </div>
      `,
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    })

    const marker = L.marker([sensor.latitude, sensor.longitude], { icon })
      .addTo(map)
      .bindPopup(`
        <div style="min-width: 200px;">
          <h3 style="font-weight: bold; margin-bottom: 8px;">${sensor.name}</h3>
          <p style="font-size: 12px; color: #666; margin-bottom: 8px;">${sensor.location_description}</p>
          ${reading ? `
            <div style="font-size: 13px;">
              <div style="margin-bottom: 4px;">
                <strong>PM2.5:</strong> ${reading.pm25?.toFixed(1) || 'N/A'} µg/m³
              </div>
              <div style="margin-bottom: 4px;">
                <strong>PM10:</strong> ${reading.pm10?.toFixed(1) || 'N/A'} µg/m³
              </div>
              <div style="margin-bottom: 4px;">
                <strong>NO₂:</strong> ${reading.no2?.toFixed(1) || 'N/A'} µg/m³
              </div>
              <div style="margin-bottom: 4px;">
                <strong>Температура:</strong> ${reading.temperature?.toFixed(1) || 'N/A'} °C
              </div>
            </div>
          ` : '<p style="color: #999;">Нет данных</p>'}
        </div>
      `)

    markers.push(marker)
  })
}
</script>

<style scoped>
/* Map marker styles are inline */
</style>
