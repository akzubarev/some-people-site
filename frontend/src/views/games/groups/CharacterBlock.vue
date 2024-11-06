<template>
  <div class="flex flex-row justify-between gap-6">
    <div class="flex flex-row gap-[3%]">
      <div class="flex w-[15%] p-4">
        <CharacterPicture :game_alias="game_alias" :src="character.image" :name="character.name"/>
      </div>
      <div class="flex flex-col w-2/3 gap-3 py-6 px-3 items-start">
        <div class="text-2xl text-content-secondary">{{ character.name }}, {{ character.alias }}</div>
        <div class="text-lg text-content-secondary-shadowed whitespace-pre-wrap"> {{ character.description }}</div>
      </div>
    </div>
    <div class="flex flex-col w-[20%] px-3 py-6 gap-1">
      <div class="text-xl text-content-secondary cursor-pointer text-center">
        {{ character.player ? character.player.name : "Свободная роль" }}
      </div>
      <div class="flex flex-row gap-3 items-center" v-if="!!character.player">
        <div class="text-xl text-content-secondary-shadowed cursor-pointer">VK</div>
        <div class="text-xl text-content-secondary-shadowed cursor-pointer">TG</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import CharacterPicture from "@/views/games/groups/CharacterPicture.vue";

const props = defineProps({
  character: {
    id: 1,
    master: 1,
    name: "lorem ipsum",
    description: "lorem ipsum",
    image: null,
    status: "active",
    applications: [],
    player: {}
  },
  full: {type: Boolean, default: true},
  game_alias: {type: String,}
})
const character = ref({
  ...props.character,
  status: "no",
})
</script>