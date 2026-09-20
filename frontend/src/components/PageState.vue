<template>
  <div class="flex flex-col items-center justify-center gap-6 p-12 min-h-screen text-center" role="status">
    <p class="text-xl">{{ message }}</p>
    <button v-if="retry" type="button" class="btn-primary" @click="reload">Попробовать снова</button>
    <router-link to="/">На главную</router-link>
  </div>
</template>
<script setup>
defineProps({message: String, retry: Boolean})
const reload = () => window.location.reload()
</script>
