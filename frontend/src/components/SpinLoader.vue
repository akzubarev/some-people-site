<template>
  <svg
    class="ip"
    viewBox="0 0 256 128"
    width="256px"
    height="128px"
    xmlns="http://www.w3.org/2000/svg"
  >
    <defs>
      <linearGradient :id="id" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#00ae3e" />
        <stop offset="33%" stop-color="#008d8e" />
        <stop offset="67%" stop-color="#0051d7" />
        <stop offset="100%" stop-color="#004cff" />
      </linearGradient>
      <linearGradient :id="id + 1" x1="1" y1="0" x2="0" y2="0">
        <stop offset="0%" stop-color="#004cff" />
        <stop offset="50%" stop-color="#06e960" />
        <stop offset="100%" stop-color="#00ae3e" />
      </linearGradient>
    </defs>
    <g fill="none" stroke-linecap="round" stroke-width="16">
      <g class="ip__track" stroke="#ddd">
        <path d="M8,64s0-56,60-56,60,112,120,112,60-56,60-56" />
        <path d="M248,64s0-56-60-56-60,112-120,112S8,64,8,64" />
      </g>
      <g stroke-dasharray="180 656">
        <path
          class="ip__worm1"
          :stroke="`url(#${id})`"
          stroke-dashoffset="0"
          d="M8,64s0-56,60-56,60,112,120,112,60-56,60-56"
        />
        <path
          class="ip__worm2"
          :stroke="`url(#${id + 1})`"
          stroke-dashoffset="358"
          d="M248,64s0-56-60-56-60,112-120,112S8,64,8,64"
        />
      </g>
    </g>
  </svg>
</template>
<style scoped>
.ip {
  width: 16em;
  height: 8em;
}
.ip__track {
  stroke: hsl(var(--hue), 90%, 90%);
  transition: stroke var(--trans-dur);
}
.ip__worm1,
.ip__worm2 {
  animation: worm1 2s linear infinite;
}
.ip__worm2 {
  animation-name: worm2;
}

/* Dark theme */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: hsl(var(--hue), 90%, 5%);
    --fg: hsl(var(--hue), 90%, 95%);
  }
  .ip__track {
    stroke: hsl(var(--hue), 90%, 15%);
  }
}

/* Animation */
@keyframes worm1 {
  from {
    stroke-dashoffset: 0;
  }
  50% {
    animation-timing-function: steps(1);
    stroke-dashoffset: -358;
  }
  50.01% {
    animation-timing-function: linear;
    stroke-dashoffset: 358;
  }
  to {
    stroke-dashoffset: 0;
  }
}
@keyframes worm2 {
  from {
    stroke-dashoffset: 358;
  }
  50% {
    stroke-dashoffset: 0;
  }
  to {
    stroke-dashoffset: -358;
  }
}
</style>
<script setup>
const id = Math.random()
</script>
