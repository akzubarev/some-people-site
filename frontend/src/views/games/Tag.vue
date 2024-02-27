<template>
  <div class="px-2 border border-1 rounded-xl text-md h-fit w-fit cursor-pointer"
       :style="`border-color: ${color} !important;
         color: ${selected ? 'white': color };
         background-color: ${selected ?  color : 'transparent'}`">
    {{ text }}
  </div>
</template>
<script setup lang="ts">
const props = defineProps(["text", "color", "selected"])
</script>
