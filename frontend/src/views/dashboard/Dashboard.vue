<template>
  <MG/>
</template>

<script setup>
import MG from "@/views/dashboard/MG.vue";


</script>


<style lang="scss">
.product-buttons {
  @apply relative flex items-end min-h-[7rem] p-4 overflow-hidden cursor-pointer;
  &.disabled {
    @apply cursor-default;
    & img {
      @apply grayscale
    }
  }
}

</style>
