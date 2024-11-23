<template>
  <div class="flex flex-col gap-3">
    <div id="top_drawer" class="flex flex-col h-full gap-6 bg-bg-transparent-white p-header p-6">
      <a class="flex flex-row items-center gap-3 text-large text-content-secondary mb-4"
         :href="`/game/${game_alias}/about`">
        <inline-svg class="w-6 h-6 rotate-180" :src="require('@/assets/images/icons/common/arrow.svg')"/>
        Назад
      </a>
      <div class="flex flex-col gap-xs">
        <div class="text-large font-semibold uppercase text-content-secondary"> Личный кабинет</div>
        <div class="text-medium uppercase text-content-secondary"> {{ user.first_name }} {{ user.last_name }}</div>
      </div>
      <div id="games" class="flex flex-col overflow-y-scroll no-scrollbar gap-medium">
        <LKGamesDrawer
            v-for="game in games.filter(g=>g.alias=='whales')" :key="game.id"
            :game_title="game.title" :game_alias="game.alias"
        />
      </div>
    </div>
    <div id="bottom_drawer" class="flex flex-col gap-6 bg-bg-transparent-white h-[60%] p-header p-6">
      <a class="text-medium font-semibold uppercase text-content-secondary" :href="`/account/settings`"> Профиль </a>
      <a class="text-medium font-semibold uppercase text-content-secondary" :href="`/sign-out`"> Выйти </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue"
import gamesService from "@/services/gamesService";
import {useStore} from "vuex";
import LKGamesDrawer from "@/views/account/drawer/LKDrawerGame.vue";


const store = useStore()
const props = defineProps(["game_alias"])
const user = store.getters['auth/user']

const games = ref([])
gamesService.games({}).then(({data}) => {
  games.value = data
})
</script>