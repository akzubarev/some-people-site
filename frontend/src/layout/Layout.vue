<template>
  <teleport to="html">
    <Loader v-if="showLoader"/>
  </teleport>
  <div class="grid">
    <!--    <Aside :class="width: 150px; box-sizing: content-box;[$style.aside, aside&&'!block']"-->
    <!--           class="hidden fixed left-0 h-full top-0 px-3" @close="aside=false"/>-->
    <!--    <div :class="max-width: theme('screens.2xl')"-->
    <div class="w-full m-auto min-h-screen h-full relative bg-bg-primary">
      <img class="absolute ml-2 mt-2 h-22 w-22 z-10 opacity-75" :src="require('@/assets/images/logo/moth.svg')"/>
      <Header @asideToggle="openAside"/>
      <router-view/>
    </div>
  </div>
  <Footer/>
</template>
<script setup>
import {onMounted, ref} from "vue"
// import Aside from "@/layout/aside/Aside.vue"
import Header from "@/layout/Header.vue"
import Footer from "@/layout/Footer.vue"
import Loader from "@/components/Loader.vue"


const showLoader = ref(true)
const aside = ref(false)

onMounted(() => {
  setTimeout(() => {
    showLoader.value = false
  }, 50)
})
const openAside = () => {
  aside.value = true
}
</script>
