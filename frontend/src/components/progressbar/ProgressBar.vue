<template>
  <div class="w-full h-32 bg-bg-primary rounded-2xl overflow-hidden">
    <div class="h-full rounded-xl bg-gradient-to-r from-gradient-start to-gradient-end"
         :style="{ width: progress + '%'}"/>
  </div>
</template>
<script setup>
defineProps({
  progress: {
    type: Number, required: true,
    validator: value => value >= 0 && value <= 100
  },
})
</script>
