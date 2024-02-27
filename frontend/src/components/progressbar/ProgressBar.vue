<template>
  <div class="w-[100%] h-32 bg-gray-700 rounded-2xl overflow-hidden">
    <div
        :class="$style.Inner" class="h-[100%] rounded-xl"
        :style="{ width: progress + '%', background: color }"
    ></div>
  </div>
</template>
<script setup>
import tailwindConfig from '@/utils/tailwindConfig'

defineProps({
  progress: {
    type: Number,
    required: true,
    validator: value => value >= 0 && value <= 100
  },
  color: {
    type: String,
    default: tailwindConfig.theme.colors.accent.green
  }
})
</script>

<style module lang="scss">

.Inner {
  transition: width 0.3s ease;
}
</style>
