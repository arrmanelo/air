<template>
  <section class="scroll-velocity-wrapper">
    <div ref="containerRef" class="scroll-velocity-container">
      <div
        v-for="(text, index) in texts"
        :key="index"
        :class="['scroll-velocity-text', className]"
        :style="{
          transform: `translateX(${baseX}%)`,
        }"
      >
        <span v-for="n in 20" :key="n" class="text-item">{{ text }} </span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface ScrollVelocityProps {
  texts: string[]
  velocity?: number
  className?: string
}

const props = withDefaults(defineProps<ScrollVelocityProps>(), {
  velocity: 5,
  className: ''
})

const containerRef = ref<HTMLDivElement | null>(null)
const baseX = ref(0)
const lastScrollY = ref(0)
const scrollVelocity = ref(0)
const directionFactor = ref(1)

let animationFrameId: number | null = null
let lastTime = Date.now()

const smoothVelocity = ref(0)
const targetVelocity = ref(0)

const lerp = (start: number, end: number, factor: number) => {
  return start + (end - start) * factor
}

const handleScroll = () => {
  const currentScrollY = window.scrollY
  const deltaY = currentScrollY - lastScrollY.value

  // Update scroll velocity
  targetVelocity.value = deltaY
  lastScrollY.value = currentScrollY

  // Update direction
  if (deltaY !== 0) {
    directionFactor.value = deltaY > 0 ? -1 : 1
  }
}

const animate = () => {
  const currentTime = Date.now()
  const deltaTime = (currentTime - lastTime) / 1000
  lastTime = currentTime

  // Smooth the velocity with spring-like interpolation
  smoothVelocity.value = lerp(smoothVelocity.value, targetVelocity.value, 0.1)
  targetVelocity.value *= 0.9 // Decay

  // Calculate movement
  const velocityFactor = smoothVelocity.value * props.velocity * 0.05
  const baseMovement = directionFactor.value * props.velocity * 0.1
  const moveBy = baseMovement + velocityFactor

  baseX.value += moveBy

  // Loop the animation
  if (baseX.value > 0) {
    baseX.value = -50
  } else if (baseX.value < -50) {
    baseX.value = 0
  }

  animationFrameId = requestAnimationFrame(animate)
}

onMounted(() => {
  lastScrollY.value = window.scrollY
  window.addEventListener('scroll', handleScroll, { passive: true })
  animationFrameId = requestAnimationFrame(animate)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId)
  }
})
</script>

<style scoped>
.scroll-velocity-wrapper {
  overflow: hidden;
  width: 100%;
  white-space: nowrap;
  position: relative;
}

.scroll-velocity-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.scroll-velocity-text {
  display: flex;
  white-space: nowrap;
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: -0.05em;
  will-change: transform;
  user-select: none;
}

.text-item {
  display: inline-block;
  margin-right: 2rem;
}

/* Text styling */
.scroll-velocity-text {
  color: white;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
