<template class="relative">
  <img class="absolute h-[300px] w-full bg-cover z-10" :src="game_images[game_alias].header"/>
  <div class="flex flex-row h-full gap-[5%] bg-whales-bg p-header px-6 h-screen w-screen pr-24">
    <LKDrawer class="w-[17.5%] z-20" :game_alias="game_alias"/>
    <router-view class="w-[75%] z-20 pt-24"/>
  </div>
</template>

<script setup lang="ts">
import {game_images} from "@/constants/gameImages";
import LKDrawer from "@/views/account/drawer/LKDrawer.vue";


const props = defineProps(["game_alias"])

</script>
