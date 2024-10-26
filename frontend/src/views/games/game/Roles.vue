<template>
  <img class="flex flex h-[200px] w-full bg-cover" :src="games[alias].header"/>
  <div class="flex flex-col gap-3 p-3">
    <div
        class="flex flex-col bg-gray-800 bg-opacity-60 gap-3 p-6 h-full min-h-screen">
      <div class="text-4xl text-white"> Сетка ролей</div>
      <div class="flex flex-col gap-3" v-if="game.factions">
        <FactionBlock
            v-for="faction in game.factions" :key="faction"
            :game="alias" :faction="faction"
        />
        <FactionBlock
            v-if="game.non_factioned.length>0" :game="alias"
            :faction="others_faction"
        />
      </div>
    </div>
  </div>
</template>


<script setup>
import {ref} from "vue"
import gamesService from "@/services/gamesService";
import FactionBlock from "@/views/games/factions/FactionBlock.vue";
import router from "@/router";
import {useStore} from "vuex";
import {games} from "@/constants/gameImages";

const store = useStore()
const props = defineProps(["alias"])
const user = store.getters['auth/user']
const game = ref({
  id: 1,
  title: "lorem ipsum",
  image: null,
  factions: [],
  non_factioned: []
})

gamesService.game(props.alias).then(({data}) => {
  if (!user.mg && !data.open_character_list)
    router.push(`/game/${data.alias}/about`)
  game.value = data
})


const others = {
  "frostpunk": {
    name: "Жители Нью-Ливерпуля",
    description: ""
  },
  "whales": {
    name: "Жители города",
    description: ""
  }
}[props.alias]
const others_faction = {
  image: null,
  name: others.name,
  description: others.description,
  characters: game.value.non_factioned, subfactions: []
}
</script>
