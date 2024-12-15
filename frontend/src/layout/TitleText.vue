<template>
  <div id="title" @click="() =>{$emit('closeDrawer'); $router.push('/')}"
       class="flex flex-row w-full items-center text-title font-semibold uppercase no-wrap cursor-pointer"
  >
    Какие-то
    <inline-svg class="h-16 md:h-24 ml-2 py-1 -mt-2 -mb-2 md:-mt-1 md:-mb-1"
                :src="require('@/assets/images/logo/mg.svg')"/>
    юди
  </div>
</template>

<script setup lang="ts">
defineEmits(['closeDrawer'])
</script>