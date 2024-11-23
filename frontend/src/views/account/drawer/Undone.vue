<template class="relative">
  <div v-if="number>0" class="h-4 w-4 text-center text-xs bg-bg-transparent rounded-full items-center">{{ number }}</div>
</template>

<script setup lang="ts">
const props = defineProps(["number"])

</script>
