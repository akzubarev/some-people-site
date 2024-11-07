<template class="relative">
  <img class="flex flex h-[300px] w-full bg-cover" :src="game_images[game_alias].header"/>
  <div class="flex flex-row bg-whales-bg">
    <GamesDrawer class="fixed z-10 w-[15%]" :game_alias="game_alias" :group_groups="group_groups"/>
    <div class="flex flex-col gap-3" v-if="group_groups">
      <div class="absolute z-0 top-[7.5rem] left-0 w-[15%] h-full bg-bg-transparent-white"/>
      <div class="absolute z-0 top-[7.5rem] left-[18%] w-[10%] h-full bg-bg-transparent-white"/>
      <div class="absolute z-0 top-[7.5rem] left-[30%] w-[55%] h-full bg-bg-transparent-white"/>
      <div class="absolute z-0 top-[7.5rem] right-0 w-[10%] h-full bg-bg-transparent-white"/>
      <GroupBlock
          class="z-10 pl-[18%]" v-for="group in group_groups.filter(g=>g.characters.length>0)"
          :key="group" :game_alias="game_alias" :group="group"
      />
      <GroupBlock class="z-10" v-if="game.non_grouped.length>0" :game_alias="game_alias" :group="others_group"/>
    </div>
  </div>
</template>


<script setup lang="ts">
import {ref} from "vue"
import gamesService from "@/services/gamesService";
import GroupBlock from "@/views/games/groups/GroupBlock.vue";
import router from "@/router";
import {useStore} from "vuex";
import {game_images} from "@/constants/gameImages";
import GamesDrawer from "@/views/games/game/GamesDrawer.vue";

const store = useStore()
const props = defineProps(['game_alias'])
const user = store.getters['auth/user']
const game = ref({
  id: 1,
  title: "lorem ipsum",
  image: null,
  groups: [],
  non_grouped: []
})
const group_groups = ref([])
const family_groups = ref([])

gamesService.game(props.game_alias).then(({data}) => {
  if (!user.mg && !data.open_character_list)
    router.push(`/game/${props.game_alias}/about`)
  game.value = data
})

gamesService.groups(props.game_alias, 'group').then(({data}) => {
  group_groups.value = data
})


const others = {
  "frostpunk": {name: "Жители Нью-Ливерпуля", description: ""},
  "whales": {name: "Жители города", description: ""}
}[props.game_alias]

const others_group = {
  image: null,
  name: others.name,
  description: others.description,
  characters: game.value.non_grouped, subgroups: []
}

</script>
