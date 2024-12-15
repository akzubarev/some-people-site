<template>
  <div class="absolute fixed left-0 top-0 h-full w-[80%] z-50 h-screen bg-whales-bg pt-6 pl-6 pr-1"
       :class="showDrawer ?  'flex flex-col gap-3' : 'hidden'" @close="showDrawer=false">
    <inline-svg
        class="absolute h-12 w-12 right-1 top-1/2 rotate-90 text-content-secondary"
        :src="require('@/assets/images/icons/common/chevrone.svg')"
        @click="$emit('close')"
    />
    <TitleText class="text-content-secondary hover:text-content-accent" @close-drawer="$emit('close')"/>
    <slot class="w-full h-full overflow-y-auto no-scrollbar"/>
  </div>
</template>

<script setup>

import TitleText from "@/layout/TitleText.vue";

defineProps(["showDrawer"])
defineEmits(['close'])
</script>
