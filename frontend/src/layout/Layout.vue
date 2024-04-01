<template>
  <teleport to="html">
    <Loader v-if="showLoader"/>
  </teleport>
  <div class="grid">
    <Aside :class="[$style.aside, aside&&'!block']"
           class="hidden fixed left-0 h-full top-0 px-3" @close="aside=false"/>
    <div :class="$style.wrapper"
         class="w-full m-auto min-h-screen h-full relative bg-[#404B5F]">
        <img class="absolute ml-2 mt-2 h-22 w-22 z-10 opacity-75"
             :src="require('@/assets/images/logos/moth.svg')"/>
      <Header @asideToggle="openAside"/>
      <router-view/>
    </div>
  </div>
</template>
<script setup>
import {onMounted, ref} from "vue"
import Aside from "@/layout/aside/Aside.vue"
import Header from "@/layout/header/Header.vue"
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
<style lang="scss" module>
$lg-layout-offset: 50px;
$aside-width: 150px;

.aside {
  width: $aside-width;
  box-sizing: content-box;
}

.wrapper {
  max-width: theme('screens.2xl');
}
</style>
