<template>
  <Popup class="popup-override" @close="$emit('close')">
    <SmallSubscription/>
  </Popup>
</template>

<style scoped lang="scss">
  .Popup .card {
    background: unset;
  }
</style>

<script setup>
  import Popup from "@/components/Popup"
  import SmallSubscription from '@/views/subscription/SmallSubscription.vue'
</script>
