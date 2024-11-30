<template class="relative">
  <img class="absolute h-[300px] w-full bg-cover z-10" :src="game_images[game_alias].header"/>
  <div class="flex flex-row h-full gap-[5%] bg-whales-bg p-header px-6 h-screen w-screen pr-24">
    <LKDrawer class="w-[30%] lg:w-[22.5%] z-20" :game_alias="game_alias"/>
    <router-view class="w-[65%] lg:w-[75%] z-20 pt-24"/>
  </div>
</template>

<script setup lang="ts">
import {game_images} from "@/constants/gameImages";
import LKDrawer from "@/views/account/drawer/LKDrawer.vue";
import gamesService from "@/services/gamesService";
import {computed} from "vue";
import {useStore} from "vuex";


const props = defineProps(["game_alias"])
const store = useStore()
const user = computed(() => store.getters["auth/user"])

gamesService.application(user.value.id, props.game_alias).then(({data}) => {
  store.dispatch("games/setApplication", data)
})
gamesService.questions(props.game_alias).then(({data}) => {
  store.dispatch("games/setQuestions", data)
})
</script>
