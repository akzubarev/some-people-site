<template>
  <img class="rounded-full border-2 border-content-primary"
       :src="src || require('@/assets/images/default_avatar.png')"/>
</template>

<script setup>
const props = defineProps({
  src: {type: String},
})
</script>
