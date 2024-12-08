<template class="relative">
  <img class="absolute h-[300px] w-full bg-cover z-10" :src="game_images[game_alias].header"/>
  <div class="flex flex-row h-full gap-[5%] bg-whales-bg p-header md:px-6 h-screen w-screen md:pr-24">
    <LKDrawer class="hidden md:flex w-[30%] lg:w-[22.5%] z-20" :game_alias="game_alias"/>
    <div class="flex flex-col gap-6 h-full">
      <div v-if="phoneScreen" class="flex flex-row items-center gap-3 z-20 px-6 md:px-0">
        <inline-svg
            class="w-6 h-6 text-header text-content-secondary rotate-180"
            @click="$router.push('/game/${game_alias}/about')"
            :src="require('@/assets/images/icons/common/arrow.svg')"
        />
        <div class="flex flex-col gap-xs">
          <div class="text-large font-semibold uppercase text-content-secondary"> Личный кабинет</div>
          <div class="text-medium uppercase text-content-secondary"> {{ user.first_name }} {{ user.last_name }}</div>
        </div>
      </div>
      <router-view class="w-full md:w-[65%] lg:w-[75%] z-20 md:p-6 md:pt-24"/>
    </div>
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
const phoneScreen = computed(() => window.screen.width < 768)
</script>
