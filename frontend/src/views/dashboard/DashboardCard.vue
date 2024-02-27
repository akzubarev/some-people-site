<template>
  <div class="card p-3" @click="$router.push(route)">
    <div :class="$style.icon">
      <slot/>
    </div>
    <div class="text-normal lg:text-xl">{{ text }}</div>
  </div>
</template>

<script setup>
const props = defineProps(["src", "route", "text"])
</script>
<style lang="scss" module>
.icon {
  justify-content: right;
  display: flex;
  svg {
    width: 64px;
    height: 64px;
  }
}
</style>