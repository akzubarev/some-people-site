<template>
  <div class="flex flex-row justify-between gap-[4%]">
    <div class="flex flex-row gap-medium w-full pr-6">
      <div class="flex w-[20%] items-center">
        <CharacterPicture :game_alias="game_alias" :src="character.image" :name="character.name"/>
      </div>
      <div class="flex flex-col w-full gap-1 items-start">
        <div class="text-medium text-content-secondary font-semibold">{{ character.name }}, {{ character.alias }}</div>
        <div class="text-sm font-semibold text-content-secondary-shadowed whitespace-pre-wrap"> {{
            character.description
          }}
        </div>
        <a v-if="personal" class="text-sm font-semibold text-content-secondary whitespace-pre-wrap"
           :href="`/game/${game_alias}/roles`">
          -> Перейти в сетку
        </a>
      </div>
    </div>
    <div v-if="!personal" class="flex flex-col w-[17.5%] ml-[2,5%] pl-6 gap-1">
      <div class="text-medium text-content-secondary sm:cursor-pointer md:cursor-default text-start">
        {{ character.player ? character.player.username : "Свободно" }}
      </div>
      <div v-if="!!character.player" class="flex flex-row gap-3 items-center pr-[2.5%] w-[10%]">
        <a class="text-medium text-content-secondary-shadowed cursor-pointer"
           :href="character.player.vk">
          VK
        </a>
        <a class="text-medium text-content-secondary-shadowed cursor-pointer"
           :href="`t.me/${character.player.telegram}`">
          TG
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import CharacterPicture from "@/views/games/roles/groups/CharacterPicture.vue";

const props = defineProps({
  character: {
    id: 1,
    master: 1,
    alias: "lorem ipsum",
    name: "lorem ipsum",
    description: "lorem ipsum",
    image: null,
    status: "active",
    applications: [],
    player: {
      username: "lorem",
      telegram: "ipsum",
      vk: "lorem",
    }
  },
  personal: {type: Boolean, default: false},
  game_alias: {type: String,}
})
const character = ref({
  ...props.character,
  status: "no",
})
</script>