<template>
  <div :class="$style.aside">
    <div class="sticky top-0">
      <div @click="$router.push('/dashboard')" class="px-3 pt-3">
        <router-link
            to="/dashboard"
        >
          <inline-svg :src="require('@/assets/images/logo/frostpunk.jpg')"/>
        </router-link>
      </div>
      <Menu @route="$emit('close')" class="mt-[50px]"/>
    </div>

    <div :class="$style.overlay" @click="$emit('close')"/>
  </div>
</template>
<script setup>
import Menu from "@/layout/aside/Menu.vue"

defineEmits(['close'])
</script>
<style lang="scss" module>
.aside {
  @apply bg-black;
  z-index: 20;
}

.overlay {
  @apply fixed h-full w-full left-0 top-0 bg-black block;
  z-index: -1;
  opacity: .3;
  @media(min-width: theme('screens.lg')) {
    @apply hidden;
  }
}
</style>
