<template>
  <section class="scroll-velocity-container">
    <div
      v-for="(text, index) in texts"
      :key="index"
      class="parallax-wrapper relative overflow-hidden py-4"
    >
      <div
        ref="scrollers"
        class="scroller flex whitespace-nowrap text-center font-sans text-4xl font-bold tracking-[-0.02em] drop-shadow md:text-[5rem] md:leading-[5rem]"
        :class="className"
        :style="{ transform: `translateX(${positions[index] || 0}px)` }"
      >
        <span
          v-for="i in numCopies"
          :key="i"
          class="flex-shrink-0"
        >
          {{ text }}&nbsp;
        </span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  texts: {
    type: Array,
    default: () => ['Scroll Text']
  },
  velocity: {
    type: Number,
    default: 100
  },
  className: {
    type: String,
    default: ''
  },
  numCopies: {
    type: Number,
    default: 6
  }
})

const scrollers = ref([])
const positions = ref([])
const basePositions = ref([])
const animationFrameId = ref(null)
let lastTime = Date.now()

const animate = () => {
  const currentTime = Date.now()
  const delta = currentTime - lastTime
  lastTime = currentTime

  props.texts.forEach((text, index) => {
    if (!basePositions.value[index]) {
      basePositions.value[index] = 0
    }

    // Alternate direction for each text
    const direction = index % 2 !== 0 ? -1 : 1
    const moveBy = direction * props.velocity * (delta / 1000)

    basePositions.value[index] += moveBy

    // Get width of one copy (assuming all copies are same width)
    const scroller = scrollers.value[index]
    if (scroller) {
      const copyWidth = scroller.scrollWidth / props.numCopies

      // Wrap position to create infinite scroll
      if (basePositions.value[index] < -copyWidth) {
        basePositions.value[index] += copyWidth
      } else if (basePositions.value[index] > 0) {
        basePositions.value[index] -= copyWidth
      }
    }

    positions.value[index] = basePositions.value[index]
  })

  animationFrameId.value = requestAnimationFrame(animate)
}

onMounted(() => {
  // Initialize positions
  positions.value = new Array(props.texts.length).fill(0)
  basePositions.value = new Array(props.texts.length).fill(0)

  // Start animation
  lastTime = Date.now()
  animate()
})

onUnmounted(() => {
  if (animationFrameId.value) {
    cancelAnimationFrame(animationFrameId.value)
  }
})
</script>

<style scoped>
.parallax-wrapper {
  background: transparent;
}

.scroller {
  will-change: transform;
}

.scroll-velocity-container {
  width: 100%;
  overflow: hidden;
}
</style>
