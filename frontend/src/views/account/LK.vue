<template class="relative">
  <img class="absolute h-[300px] w-full bg-cover z-10" :src="game_images[game_alias].header"/>
  <Drawer :show-drawer="showDrawer" @close="showDrawer=false">
    <LKDrawer class="h-full" :game_alias="game_alias" @close-drawer="showDrawer=false"/>
  </Drawer>
  <div class="flex flex-row h-full gap-[5%] bg-whales-bg p-header md:px-6 h-screen w-screen md:pr-24">
    <LKDrawer class="hidden md:flex w-[30%] lg:w-[22.5%] z-20" :game_alias="game_alias"/>
    <div class="flex flex-col gap-6 md:w-[65%] lg:w-[75%] h-full mt-6 md:mt-0">
      <div v-if="phoneScreen" class="flex flex-row items-center gap-3 z-20 px-6 md:px-0">
        <inline-svg
            class="w-8 h-8 text-header text-content-secondary cursor-pointer"
            @click="showDrawer=true" :src="require('@/assets/images/icons/common/menu.svg')"
        />
        <div class="flex flex-col gap-xs">
          <div class="text-large font-semibold uppercase text-content-secondary"> Личный кабинет</div>
          <div class="text-medium uppercase text-content-secondary"> {{ user.first_name }} {{ user.last_name }}</div>
        </div>
      </div>
      <router-view class="w-full h-full z-20 md:p-6 md:pt-24"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import {game_images} from "@/constants/gameImages";
import LKDrawer from "@/views/account/drawer/LKDrawer.vue";
import gamesService from "@/services/gamesService";
import {computed, ref} from "vue";
import {useStore} from "vuex";
import Drawer from "@/layout/Drawer.vue"

const props = defineProps(["game_alias"])
const store = useStore()
const user = computed(() => store.getters["auth/user"])
const showDrawer = ref(false)

gamesService.application(user.value.id, props.game_alias).then(({data}) => {
  store.dispatch("games/setApplication", data)
})
gamesService.questions(props.game_alias).then(({data}) => {
  store.dispatch("games/setQuestions", data)
})
const phoneScreen = ref(window.innerWidth < 768)
const updateWidth = () => phoneScreen.value = window.innerWidth < 768
const onLeave = () => {
  window.removeEventListener('resize', updateWidth);
  window.removeEventListener('beforeunload', onLeave);
}
window.addEventListener('resize', updateWidth)
window.addEventListener('beforeunload', onLeave)
</script>
