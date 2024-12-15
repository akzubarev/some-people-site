<template>
  <teleport to="html">
    <Loader v-if="showLoader"/>
  </teleport>
  <div class="grid">
    <div class="w-full m-auto min-h-screen h-full relative bg-bg-primary">
      <Header/>
      <router-view/>
    </div>
  </div>
</template>
<script setup>
import {onMounted, ref} from "vue"
import Header from "@/layout/Header.vue"
import Loader from "@/components/Loader.vue"


const showLoader = ref(true)

onMounted(() => {
  setTimeout(() => {
    showLoader.value = false
  }, 50)
})
</script>
