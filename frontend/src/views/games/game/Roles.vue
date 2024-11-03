<template>
  <img class="flex flex h-[200px] w-full bg-cover" :src="game_images[alias].header"/>
  <div class="flex flex-col gap-3 p-3">
    <div
        class="flex flex-col bg-gray-800 bg-opacity-60 gap-3 p-6 h-full min-h-screen">
      <div class="text-4xl"> Сетка ролей</div>
      <div class="flex flex-col gap-3" v-if="game.groups">
        <GroupBlock
            v-for="group in game.groups" :key="group"
            :game="alias" :group="group"
        />
        <GroupBlock
            v-if="game.non_grouped.length>0" :game="alias"
            :group="others_group"
        />
      </div>
    </div>
  </div>
</template>


<script setup>
import {ref} from "vue"
import gamesService from "@/services/gamesService";
import GroupBlock from "@/views/games/groups/GroupBlock.vue";
import router from "@/router";
import {useStore} from "vuex";
import {game_images} from "@/constants/gameImages";

const store = useStore()
const props = defineProps(["alias"])
const user = store.getters['auth/user']
const game = ref({
  id: 1,
  title: "lorem ipsum",
  image: null,
  groups: [],
  non_grouped: []
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
const others_group = {
  image: null,
  name: others.name,
  description: others.description,
  characters: game.value.non_grouped, subgroups: []
}
</script>
